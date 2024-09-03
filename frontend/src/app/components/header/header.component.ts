import { Router, RouterOutlet } from '@angular/router';
import { ButtonComponent } from '../button/button.component';
import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [ButtonComponent, RouterOutlet, CommonModule],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss',
})
export class HeaderComponent {
  public authService = inject(AuthService);
  private router = inject(Router);

  openLoginModal() {
    this.router.navigate([{ outlets: { modal: ['modal', 'login'] } }]);
  }
}
