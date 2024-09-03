import { Component } from '@angular/core';
import { PriceComponent } from "../price/price.component";
import { RatingComponent } from "../rating/rating.component";

@Component({
  selector: 'app-product-item',
  standalone: true,
  imports: [PriceComponent, RatingComponent],
  templateUrl: './product-item.component.html',
  styleUrl: './product-item.component.scss'
})
export class ProductItemComponent {

}
