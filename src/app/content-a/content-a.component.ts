import { ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
  selector: 'app-content-a',
  standalone: true,
  imports: [],
  templateUrl: './content-a.component.html',
  styleUrl: './content-a.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ContentAComponent {}
