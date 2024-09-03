import { InputAutocomplete } from '../../enums/input-autocomplete.enum';
import { Component, input, output } from '@angular/core';
import { InputType } from '../../enums/input-type.enum';
import { FormControl, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-form-input',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './form-input.component.html',
  styleUrl: './form-input.component.scss',
})
export class FormInputComponent {
  control = input.required<FormControl>();
  type = input.required<InputType>();
  
  autocomplete = input<InputAutocomplete>();
  errorMessage = input<string>();
  placeholder = input<string>();
  name = input<string>();

  value = output<string>();

  returnValue(event: Event) {
    const value = (event.target as HTMLInputElement).value;
    this.value.emit(value);
  }
}
