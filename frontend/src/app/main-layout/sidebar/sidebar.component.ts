import { MenuItem } from 'primeng/api';
import { TieredMenuModule } from 'primeng/tieredmenu';
import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, computed, inject } from "@angular/core";
import { RouterLink, RouterOutlet } from '@angular/router';
import { AuthService } from "../../api/auth.service";

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, TieredMenuModule],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SidebarComponent {
  auth = inject(AuthService);

  items = computed<MenuItem[]>(() => {
    return [
      {
        label: 'Component A',
        route: '/component-a',
      },
      {
        label: 'Component B',
        route: '/component-b',
      },
      {
        label: 'Products',
        items: [
          {
            label: 'New',
          },
          {
            label: 'Search',
          },
        ],
      },
      {
        label: 'Profile',
        items: [
          {
            label: 'Settings',
          },
          {
            label: 'Logout',
            visible: this.auth.isAuthenticated(),
          },
          {
            label: 'Login',
            route: '/login',
            visible: this.auth.isGuest(),
          },
          {
            label: 'Register',
            route: '/register',
            visible: this.auth.isGuest(),
          }
        ],
      },
    ];
  });
}
