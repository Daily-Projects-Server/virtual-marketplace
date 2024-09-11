import { ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
  selector: 'app-content-b',
  standalone: true,
  imports: [],
  templateUrl: './content-b.component.html',
  styleUrl: './content-b.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ContentBComponent {}
