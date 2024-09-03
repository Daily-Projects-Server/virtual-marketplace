import { FormInputComponent } from '../form-input/form-input.component';
import { InputAutocomplete } from '../../enums/input-autocomplete.enum';
import { ButtonComponent } from '../button/button.component';
import { AuthService } from '../../services/auth.service';
import { InputType } from '../../enums/input-type.enum';
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';
import { ButtonType } from '../../enums/button-type.enum';

@Component({
  selector: 'app-login-form',
  standalone: true,
  imports: [FormInputComponent, ButtonComponent, ReactiveFormsModule],
  templateUrl: './login-form.component.html',
  styleUrl: './login-form.component.scss',
  providers: [AuthService],
})
export class LoginFormComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  loginForm = new FormGroup({
    password: new FormControl<string>('', [
      Validators.required,
      Validators.minLength(8),
    ]),
    email: new FormControl<string>('', [
      Validators.pattern('[a-z0-9._%+-]+@[a-z0-9.-]+[.][a-z]{2,4}$'),
      Validators.required,
    ]),
  });

  InputAutocomplete = InputAutocomplete;
  ButtonType = ButtonType;
  InputType = InputType;

  // Change modal to registration
  showRegisterModal() {
    this.router.navigate([{ outlets: { modal: ['modal', 'register'] } }]);
  }

  closeModal() {
    this.router.navigate([{ outlets: { modal: null } }]);
  }

  onSubmit() {
    console.warn(this.loginForm.value);
    // this.authService.login(this.loginValues).subscribe({
    //   next: (data) => {
    //     // TODO condition for login
    //     if (data) {
    //       this.authService.setLoggedIn(true);
    //       this.closeModal();
    //     }
    //   },
    // })
  }
}
