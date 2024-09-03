import { Component, input } from '@angular/core';

@Component({
  selector: 'app-rating',
  standalone: true,
  imports: [],
  templateUrl: './rating.component.html',
  styleUrl: './rating.component.scss'
})
export class RatingComponent {
  // If maximum is given, the component will render number of stars out of maximum
  maximum = input<number>();
  rating = input<number>(0);

  fakeArray: number[] = [];

  ngAfterContentInit() {
    this.fakeArray = new Array(Math.floor(this.rating()));
  }
}
