import { Component, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

export interface StoredItem {
  id: string;
  name: string;
  widthMm: number;
  depthMm: number;
  heightMm: number;
  quantity: number;
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'stow';
  text: string;
  timestamp: Date;
  suggestedAction?: string;
  isOversizedAlert?: boolean;
}

@Component({
  selector: 'app-stow-assistant',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './stow-assistant.html',
  styleUrl: './stow-assistant.css'
})
export class StowAssistant {
  // Locale State (Fix for Finding 3)
  currentLocale = signal<'vi' | 'en'>('vi');

  // Chat Messages
  messages = signal<ChatMessage[]>([
    {
      id: '1',
      sender: 'stow',
      text: 'Xin chào! Em là STOW 2.0 - Trợ lý AI nâng cấp của MyStorage. Em đã cập nhật chuẩn dữ liệu llms.txt (giá kho từ 559.000đ/tháng, bảo hiểm 500k/CBM tối đa 10 trđ). Anh/chị cần tư vấn hay ước tính đồ đạc lưu kho ạ?',
      timestamp: new Date()
    }
  ]);

  userInput = signal<string>('');

  // Item Manager State
  items = signal<StoredItem[]>([
    { id: 'item-1', name: 'Thùng carton tiêu chuẩn (L)', widthMm: 600, depthMm: 400, heightMm: 400, quantity: 5 },
    { id: 'item-2', name: 'Tủ lạnh 2 cánh (Side-by-side)', widthMm: 900, depthMm: 750, heightMm: 1800, quantity: 1 }
  ]);

  // Form inputs for adding custom item
  newItemName = '';
  newItemWidth = 600;
  newItemDepth = 400;
  newItemHeight = 500;
  newItemQty = 1;

  // Presets
  presets = [
    { name: 'Thùng carton L', w: 600, d: 400, h: 400 },
    { name: 'Sofa 3 chỗ', w: 2000, d: 900, h: 850 },
    { name: 'Máy giặt cửa trước', w: 600, d: 650, h: 850 },
    { name: 'Tủ áo cao cấp (>2m)', w: 1200, d: 600, h: 2400 }, // Triggers Finding 2 Fix
    { name: 'Bàn làm việc', w: 1400, d: 700, h: 750 }
  ];

  // Calculated Metrics
  totalVolumeCbm = computed(() => {
    return this.items().reduce((acc, item) => {
      const volOne = (item.widthMm / 1000) * (item.depthMm / 1000) * (item.heightMm / 1000);
      return acc + (volOne * item.quantity);
    }, 0);
  });

  // Check for oversized items (> 2000mm height)
  hasOversizedItems = computed(() => {
    return this.items().some(item => item.heightMm > 2000);
  });

  oversizedItemNames = computed(() => {
    return this.items().filter(item => item.heightMm > 2000).map(i => i.name).join(', ');
  });

  // Recommended Storage Solution based on llms.txt rules
  recommendedSolution = computed(() => {
    const cbm = this.totalVolumeCbm();
    const isOversized = this.hasOversizedItems();

    if (isOversized) {
      return {
        type: 'Dong Nai Shelf-Space Warehouse (Full Service)',
        sizeStr: `${cbm.toFixed(2)} m³ (Đặc thù chiều cao > 2m)`,
        priceEst: Math.max(559000, Math.ceil(cbm * 280000)),
        facility: 'Nhón Trạch 3, Đồng Nai (Có xe đưa đón tận nơi)',
        isOversizedFallback: true
      };
    }

    if (cbm <= 1.5) {
      return {
        type: 'Private Self-Storage Locker (1.5 CBM)',
        sizeStr: '1.5 m³ (1m x 1m x 1.5m)',
        priceEst: 559000,
        facility: '375 Võ Nguyên Giáp, An Khánh hoặc Ministop D1/D7',
        isOversizedFallback: false
      };
    } else if (cbm <= 4.0) {
      return {
        type: 'Self-Storage Room (4 CBM)',
        sizeStr: '4 m³ (1.5m x 1.5m x 1.8m)',
        priceEst: 1190000,
        facility: '375 Võ Nguyên Giáp, An Phú Sports Park',
        isOversizedFallback: false
      };
    } else {
      return {
        type: 'Large Storage Unit (8-23 CBM)',
        sizeStr: `${Math.ceil(cbm)} m³`,
        priceEst: Math.ceil(cbm * 260000),
        facility: 'Kho HQ 375 Võ Nguyên Giáp, Thủ Đức',
        isOversizedFallback: false
      };
    }
  });

  // Basic Protection Insurance Calculation (Fixed Ground Truth)
  insuranceCoverage = computed(() => {
    const cbm = this.totalVolumeCbm();
    const basicLimit = Math.min(10000000, Math.ceil(cbm * 500000));
    return {
      freeTier: 'Gói Cơ Bản (Miễn phí)',
      maxCoverageVnd: basicLimit.toLocaleString('vi-VN') + ' VNĐ',
      formula: `${cbm.toFixed(1)} m³ × 500.000đ/CBM (Tối đa 10.000.000đ)`
    };
  });

  // Switch Locale
  toggleLocale(lang: 'vi' | 'en') {
    this.currentLocale.set(lang);
    const greeting = lang === 'en' 
      ? 'Switched locale to English. STOW 2.0 system state and prompt context synced.'
      : 'Đã chuyển sang Tiếng Việt. Dữ liệu ngữ cảnh hệ thống STOW 2.0 đã đồng bộ.';
    this.addStowMessage(greeting);
  }

  // Add Item
  addItem() {
    if (!this.newItemName.trim()) return;
    const newItem: StoredItem = {
      id: 'item-' + Date.now(),
      name: this.newItemName.trim(),
      widthMm: Number(this.newItemWidth),
      depthMm: Number(this.newItemDepth),
      heightMm: Number(this.newItemHeight),
      quantity: Number(this.newItemQty)
    };
    this.items.update(list => [...list, newItem]);
    
    if (newItem.heightMm > 2000) {
      this.addStowMessage(
        `⚠️ Cảnh báo đồ quá khổ: Đồ vật "${newItem.name}" có chiều cao ${newItem.heightMm}mm (> 2000mm). STOW 2.0 tự động kích hoạt đề xuất Kho Shelf Space tại Nhơn Trạch 3 (Đồng Nai) có hỗ trợ xe đưa đón!`,
        true
      );
    }

    this.resetForm();
  }

  applyPreset(preset: { name: string; w: number; d: number; h: number }) {
    this.newItemName = preset.name;
    this.newItemWidth = preset.w;
    this.newItemDepth = preset.d;
    this.newItemHeight = preset.h;
  }

  removeItem(id: string) {
    this.items.update(list => list.filter(i => i.id !== id));
  }

  // Send Chat Message
  sendMessage() {
    const text = this.userInput().trim();
    if (!text) return;

    // Add user message
    this.messages.update(m => [...m, {
      id: 'msg-' + Date.now(),
      sender: 'user',
      text,
      timestamp: new Date()
    }]);

    this.userInput.set('');

    // Generate STOW Response based on Ground Truth (llms.txt)
    setTimeout(() => {
      let reply = '';
      const lower = text.toLowerCase();

      if (lower.includes('giá') || lower.includes('bao nhiêu') || lower.includes('price') || lower.includes('cost')) {
        reply = `Theo chuẩn thông tin chính thức của MyStorage (llms.txt):\n- Kho máy lạnh / kho đồ gia dụng nhỏ nhất giá từ 559.000 VNĐ/tháng (~21 USD).\n- Kho gửi hành lý theo giờ từ 54.000 VNĐ/giờ.\n- Hiện tại danh sách đồ của bạn (${this.totalVolumeCbm().toFixed(2)} m³) ước tính hết ${this.recommendedSolution().priceEst.toLocaleString('vi-VN')} VNĐ/tháng cho gói ${this.recommendedSolution().type}.`;
      } else if (lower.includes('bảo hiểm') || lower.includes('mất mát') || lower.includes('insurance')) {
        reply = `Chính sách bảo hiểm của MyStorage:\n- Gói cơ bản MIỄN PHÍ bảo vệ 500.000 VNĐ/CBM, tối đa 10.000.000 VNĐ cho toàn bộ kho.\n- Đối với đồ đạc của bạn (${this.totalVolumeCbm().toFixed(2)} m³), bảo hiểm cơ bản được đền bù tối đa ${this.insuranceCoverage().maxCoverageVnd}.\n- Có các gói Nâng cao Silver, Gold, Platinum đền bù lên đến 100.000.000 VNĐ.`;
      } else if (lower.includes('địa chỉ') || lower.includes('kho') || lower.includes('location')) {
        reply = `MyStorage có 8 chi nhánh kho tại TP.HCM & Đồng Nai:\n1. HQ: 375 Võ Nguyên Giáp, An Khánh, TP. Thủ Đức.\n2. An Phú Sports Park: 90 Song Hành.\n3. Locker 24/7: Ministop Trần Khắc Chân (D1), Ministop Trần Trọng Cung (D7), Centre Mall (D6), Ministop MT Eastmark (D9).\n4. Kho Shelf-Space lớn: KCN Nhơn Trạch 3, Đồng Nai (chuyên chở đồ lớn/quá khổ).`;
      } else {
        reply = `STOW 2.0 đã ghi nhận yêu cầu: "${text}". Dựa trên ${this.items().length} món đồ đạc của bạn (tổng thể tích ${this.totalVolumeCbm().toFixed(2)} m³), gói đề xuất là ${this.recommendedSolution().type} tại ${this.recommendedSolution().facility}.`;
      }

      this.addStowMessage(reply);
    }, 400);
  }

  private addStowMessage(text: string, isOversizedAlert = false) {
    this.messages.update(m => [...m, {
      id: 'stow-' + Date.now(),
      sender: 'stow',
      text,
      timestamp: new Date(),
      isOversizedAlert
    }]);
  }

  private resetForm() {
    this.newItemName = '';
    this.newItemWidth = 600;
    this.newItemDepth = 400;
    this.newItemHeight = 500;
    this.newItemQty = 1;
  }
}
