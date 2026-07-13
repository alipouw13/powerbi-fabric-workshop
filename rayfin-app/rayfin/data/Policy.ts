import {
  entity,
  authenticated,
  role,
  text,
  int,
  date,
  uuid,
  set,
  one,
  many,
} from '@microsoft/rayfin-core';

import { Customer } from './Customer.js';
import { Agent } from './Agent.js';
import { Claim } from './Claim.js';

// A written policy. The @role policy scopes writes to the agent who owns the
// book: an agent can only create/update policies where agentUserId matches their
// signed-in subject. This is the Rayfin equivalent of Power BI row-level
// security, and a nice teaching parallel in the workshop.
@entity()
@authenticated('*')
@role('authenticated', 'write', {
  policy: (claims, item) => claims.sub.eq(item.agentUserId),
})
export class Policy {
  @uuid() id!: string;
  @text({ max: 40 }) policyNumber!: string;
  @set('Auto', 'Home', 'Renters', 'Life', 'Umbrella')
  product!: 'Auto' | 'Home' | 'Renters' | 'Life' | 'Umbrella';
  @set('Northeast', 'Southeast', 'Midwest', 'Southwest', 'West')
  region!: 'Northeast' | 'Southeast' | 'Midwest' | 'Southwest' | 'West';
  @set('Independent Agent', 'Captive Agent', 'Direct', 'Online')
  channel!: 'Independent Agent' | 'Captive Agent' | 'Direct' | 'Online';
  @int() annualPremium!: number;
  @set('In Force', 'Lapsed', 'Cancelled')
  status!: 'In Force' | 'Lapsed' | 'Cancelled';
  @date() effectiveDate!: Date;
  @one(() => Customer) customer!: Customer;
  @one(() => Agent) agent!: Agent;
  // Owning agent's signed-in subject, used by the RLS policy above.
  @text({ max: 120 }) agentUserId!: string;
  @many(() => Claim) claims?: Claim[];
  @date() createdAt!: Date;
}
