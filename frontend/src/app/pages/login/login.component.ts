import { ChangeDetectionStrategy, Component, inject } from "@angular/core";
import { FormComponent } from "../../forms";
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from "@angular/forms";
import { InputTextModule } from "primeng/inputtext";
import { AuthService } from "../../api/auth.service";
import { takeUntilDestroyed } from "@angular/core/rxjs-interop";
import { take } from "rxjs";

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    FormComponent,
    ReactiveFormsModule,
    InputTextModule
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LoginComponent {
  private authApi = inject(AuthService);
  form = new FormGroup({
    email: new FormControl('chris@chrisperko.net', [Validators.required, Validators.email]),
    password: new FormControl('password', [Validators.required]),
  })

  // todo: handle error messages from the server

  submitLoginForm() {
    this.form.markAllAsTouched();
    this.form.updateValueAndValidity();

    if (this.form.valid && this.form.value.email && this.form.value.password) {
      console.log('Form is valid');
      this.authApi.login(this.form.value.email, this.form.value.password).pipe(
        take(1)
      ).subscribe();
    } else {
      console.log('Form is invalid');
    }
  }
}
