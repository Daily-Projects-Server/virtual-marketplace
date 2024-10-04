import { ChangeDetectionStrategy, Component, input, output } from "@angular/core";
import { Button } from "primeng/button";

@Component({
  selector: 'form[appForm]',
  standalone: true,
  imports: [
    Button
  ],
  templateUrl: './form.component.html',
  styleUrl: './form.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FormComponent {
  label = input('Submit');
  submit = output();
}
