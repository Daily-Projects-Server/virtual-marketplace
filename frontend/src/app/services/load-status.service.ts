import { computed, Injectable, signal } from "@angular/core";

type LoadStatus = 'idle' | 'loading' | 'success' | 'error';

@Injectable()
export class LoadStatusService {

  private status = signal<LoadStatus>('idle');

  isIdle = computed(() => this.status() === 'idle');
  isLoading = computed(() => this.status() === 'loading');
  isSuccess = computed(() => this.status() === 'success');
  isError = computed(() => this.status() === 'error');

  setLoading() {
    this.status.set('loading');
  }

  setSuccess() {
    this.status.set('success');
  }

  setError() {
    this.status.set('error');
  }

  reset() {
    this.status.set('idle');
  }

}
