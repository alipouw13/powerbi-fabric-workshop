import { entity, authenticated, text, int, uuid, set } from '@microsoft/rayfin-core';

// A policyholder. Read access is open to any authenticated user in this workshop
// app; tighten with @role in a real deployment.
@entity()
@authenticated('*')
export class Customer {
  @uuid() id!: string;
  @text({ max: 120 }) name!: string;
  @set('Personal', 'Preferred', 'High Net Worth', 'Small Business')
  segment!: 'Personal' | 'Preferred' | 'High Net Worth' | 'Small Business';
  @set('Northeast', 'Southeast', 'Midwest', 'Southwest', 'West')
  region!: 'Northeast' | 'Southeast' | 'Midwest' | 'Southwest' | 'West';
  @int() tenureYears!: number;
}
