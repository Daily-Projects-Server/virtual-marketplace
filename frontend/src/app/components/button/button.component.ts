import { Component, input, output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ButtonType } from '../../enums/button-type.enum';

@Component({
  selector: 'app-button',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './button.component.html',
  styleUrl: './button.component.scss',
})
export class ButtonComponent {
  type = input<ButtonType>(ButtonType.SUBMIT);
  buttonFunction = output<void>();
  disabled = input<boolean>();
  route = input<string>();

  onClick() {
    this.buttonFunction.emit();
  }
}
