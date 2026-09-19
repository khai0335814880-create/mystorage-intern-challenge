import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StowAssistant } from './stow-assistant/stow-assistant';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, StowAssistant],
  templateUrl: './app.html'
})
export class App {}
