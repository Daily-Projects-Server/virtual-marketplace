import { ChangeDetectionStrategy, Component, inject } from "@angular/core";
import { FormComponent } from "../../forms";
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from "@angular/forms";
import { InputTextModule } from "primeng/inputtext";
import { AuthService } from "../../api/auth.service";
import { catchError, EMPTY, take } from "rxjs";
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

  submitLoginForm() {
    this.form.markAllAsTouched();
    this.form.updateValueAndValidity();

    if (this.form.valid && this.form.value.email && this.form.value.password) {
      this.loadStatus.setLoading();
      this.authApi.login(this.form.value.email, this.form.value.password).pipe(
        take(1),
        catchError(() => {
          this.loadStatus.setError();
          return EMPTY;
        })
      ).subscribe(() => this.loadStatus.setSuccess());
    } else {
      console.error('Form is invalid');
    }
  }
}
