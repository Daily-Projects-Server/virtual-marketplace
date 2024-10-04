import { ChangeDetectionStrategy, Component, inject } from "@angular/core";
import { FormComponent } from "../../forms";
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from "@angular/forms";
import { InputTextModule } from "primeng/inputtext";
import { AuthService } from "../../api/auth.service";
import { take } from "rxjs";
import { LoadStatusService } from "../../services/load-status.service";
import { ProgressBarModule } from "primeng/progressbar";
import { ProgressSpinnerModule } from "primeng/progressspinner";

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    FormComponent,
    ReactiveFormsModule,
    InputTextModule,
    ProgressBarModule,
    ProgressSpinnerModule
  ],
  providers: [LoadStatusService],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LoginComponent {
  private authApi = inject(AuthService);
  protected loadStatus = inject(LoadStatusService);

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
      this.loadStatus.setLoading();
      this.authApi.login(this.form.value.email, this.form.value.password).pipe(
        take(1),
      ).subscribe(() => this.loadStatus.setSuccess());
    } else {
      console.log('Form is invalid');
    }
  }
}
