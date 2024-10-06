import { ChangeDetectionStrategy, Component, inject, input, output } from "@angular/core";
import { Button } from "primeng/button";
import { LoadStatusService } from "../../services/load-status.service";

@Component({
  selector: 'form[appForm]',
  standalone: true,
  imports: [
    Button
  ],
  styleUrl: './form.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <ng-content />
    <p-button [label]="label()" (click)="submit.emit()" [disabled]="loadStatus.isLoading()" />
    @if (loadStatus.isError()) {
      <p>An error has occurred.</p>
    }
  `
})
export class FormComponent {
  label = input('Submit');
  submit = output();
  loadStatus = inject(LoadStatusService);
}
