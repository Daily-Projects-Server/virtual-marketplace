import { computed, inject, Injectable, signal } from "@angular/core";
import { DOCUMENT } from "@angular/common";
import { HttpClient } from "@angular/common/http";
import { environment } from "../../environments/environment";
import { RegisterDTO } from "../models";
import { tap } from "rxjs";

export type LoginResponse = {
  access_token: string;
  message: string;
  response: string;
}

@Injectable({
  providedIn: "root"
})
export class AuthService {

  private http = inject(HttpClient);
  private environment = environment;
  private DOCUMENT = inject(DOCUMENT);
  localStorage = this.DOCUMENT.defaultView?.localStorage;

  private _token = signal<string>("");
  token = this._token.asReadonly();
  isAuthenticated = computed(() => !!this._token());
  isGuest = computed(() => !this.isAuthenticated());

  constructor() {
    const token = this.localStorage?.getItem("access_token");
    if (token) {
      this._token.set(token);
    }
  }

  login(email: string, password: string) {
    return this.http.post<LoginResponse>(`${this.environment.api}/login/`, { email, password }).pipe(
      tap(({ access_token }) => {
        this.localStorage?.setItem("access_token", access_token);
        this._token.set(access_token);
      })
    );
  }

  register(dto: RegisterDTO) {
    return this.http.post(`${this.environment.api}/register/`, dto);
  }
}
