import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable, timeout } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  // TODO: change url
  private url = 'https://api.restful-api.dev/objects';
  private http = inject(HttpClient);

  isLoggedIn: boolean = false;

  constructor() {
    // check if user is logged in
    if (typeof window !== 'undefined' && window.localStorage) {
      const savedState = window.localStorage.getItem('isLoggedIn') === 'true';
      this.isLoggedIn = savedState;
    }
  }

  login(loginObject: { email: string; password: string }): Observable<any> {
    return this.http.post<any>(`${this.url}`, loginObject);
  }

  register(registerObject: {
    firstName: string;
    lastName: string;
    password: string;
    email: string;
  }): Observable<any> {
    return this.http.post<any>(`${this.url}`, registerObject);
  }

  // Change LogIn to true
  setLoggedIn(value: boolean): void {
    localStorage.setItem('isLoggedIn', JSON.stringify(value));
    this.isLoggedIn = value;
    setTimeout(() => {
      window.location.reload();
    })
  }
}
