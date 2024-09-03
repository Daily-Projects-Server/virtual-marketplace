import { Component } from '@angular/core';

@Component({
  selector: 'app-horizontal-product-slider',
  standalone: true,
  imports: [],
  templateUrl: './horizontal-product-slider.component.html',
  styleUrl: './horizontal-product-slider.component.scss'
})
export class HorizontalProductSliderComponent {
  items: any[] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15];
}
