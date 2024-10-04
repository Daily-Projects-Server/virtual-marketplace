import { TestBed } from '@angular/core/testing';

import { LoadStatusService } from './load-status.service';

describe('LoadStatusService', () => {
  let service: LoadStatusService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LoadStatusService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
