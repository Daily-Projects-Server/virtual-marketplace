import { FormInputComponent } from '../form-input/form-input.component';
import { InputAutocomplete } from '../../enums/input-autocomplete.enum';
import { ButtonComponent } from '../button/button.component';
import { AuthService } from '../../services/auth.service';
import { InputType } from '../../enums/input-type.enum';
import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { ButtonType } from '../../enums/button-type.enum';

@Component({
  selector: 'app-register-form',
  standalone: true,
  imports: [FormInputComponent, ButtonComponent, ReactiveFormsModule],
  templateUrl: './register-form.component.html',
  styleUrl: './register-form.component.scss',
})
export class RegisterFormComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  registerForm = new FormGroup({
    firstName: new FormControl<string>('', [
      Validators.pattern("^[A-Za-z]+['\\-]{0,1}[A-Za-z]*[A-Za-z]$"),
      Validators.minLength(3),
      Validators.required,
    ]),
    lastName: new FormControl<string>('', [
      Validators.pattern("^[A-Za-z]+['\\-]{0,1}[A-Za-z]*[A-Za-z]$"),
      Validators.minLength(3),
      Validators.required,
    ]),
    password: new FormControl<string>('', [
      Validators.minLength(8),
      Validators.required,
    ]),
    email: new FormControl<string>('', [
      Validators.pattern('[a-z0-9._%+-S]+@[a-z0-9.-S]+.[a-z]{0,2}$'),
      Validators.minLength(3),
      Validators.required,
    ]),
  });

  InputAutocomplete = InputAutocomplete;
  ButtonType = ButtonType;
  InputType = InputType;

  // Change modal to login
  showLoginModal() {
    this.router.navigate([{ outlets: { modal: ['modal', 'login'] } }]);
  }

  closeModal() {
    this.router.navigate([{ outlets: { modal: null } }]);
  }

  onSubmit() {
    console.warn(this.registerForm.value);
    // this.authService.register(this.registerForm.value).subscribe({
    //   next: (data) => {
    //     // TODO condition for register
    //     if (data) {
    //       this.authService.setLoggedIn(true);
    //       this.closeModal();
    //     }
    //   },
    // })
  }
}
