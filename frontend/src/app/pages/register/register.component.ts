import { ChangeDetectionStrategy, Component, inject } from "@angular/core";
import { FormComponent } from "../../forms";
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from "@angular/forms";
import { InputTextModule } from "primeng/inputtext";
import { RegisterDTO } from "../../models";
import { AuthService } from "../../api/auth.service";

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    FormComponent,
    FormsModule,
    InputTextModule,
    ReactiveFormsModule
  ],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class RegisterComponent {
  private authApi = inject(AuthService);

  form = new FormGroup({
    email: new FormControl('', [Validators.required, Validators.email]),
    firstName: new FormControl('', [Validators.required]),
    lastName: new FormControl('', [Validators.required]),
    password: new FormControl('', [Validators.required]),
    confirmPassword: new FormControl('', [Validators.required]),
  });

  // todo: show error messages from the server
  // todo: redirect to login page after successful registration

  submitRegistrationForm() {
    this.form.markAllAsTouched();
    this.form.updateValueAndValidity();

    if (this.form.valid) {
      const dto = {
        email: this.form.value.email ?? '',
        first_name: this.form.value.firstName ?? '',
        last_name: this.form.value.lastName ?? '',
        password: this.form.value.password ?? '',
        confirm_password: this.form.value.confirmPassword ?? ''
      } as RegisterDTO;
      this.authApi.register(dto).subscribe();
    }
  }
}
