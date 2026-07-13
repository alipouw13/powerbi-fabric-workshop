import { entity, authenticated, text, uuid, set } from '@microsoft/rayfin-core';

// A selling agent. `userId` links the agent to a signed-in identity so policies
// and claims can be row-level-secured to "my book" (see Policy.ts).
@entity()
@authenticated('*')
export class Agent {
  @uuid() id!: string;
  @text({ max: 120 }) name!: string;
  @text({ max: 120 }) agency!: string;
  @set('Northeast', 'Southeast', 'Midwest', 'Southwest', 'West')
  region!: 'Northeast' | 'Southeast' | 'Midwest' | 'Southwest' | 'West';
  @set('Independent Agent', 'Captive Agent', 'Direct', 'Online')
  channel!: 'Independent Agent' | 'Captive Agent' | 'Direct' | 'Online';
  // Signed-in subject (claims.sub) of the agent, used by the RLS policy.
  @text({ max: 120, optional: true }) userId?: string;
}
