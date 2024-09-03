import { Component, ElementRef, inject, ViewChild } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-modal',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './modal.component.html',
  styleUrl: './modal.component.scss',
})
export class ModalComponent {
  @ViewChild('modal') modal: ElementRef | undefined;
  
  private router = inject(Router);

  closeModal() {
    this.router.navigate([{ outlets: { modal: null } }]);
  }

  onBackdropClick(event: MouseEvent) {
    if (event.target === this.modal?.nativeElement) {
      this.closeModal();
    }
  }
}
