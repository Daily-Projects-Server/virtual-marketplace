import { MenuItem } from 'primeng/api';
import { TieredMenuModule } from 'primeng/tieredmenu';

import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, TieredMenuModule],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SidebarComponent {
  items: MenuItem[] = [
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
        },
      ],
    },
  ];
}
