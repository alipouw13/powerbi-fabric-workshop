import {
  entity,
  authenticated,
  text,
  int,
  date,
  uuid,
  set,
  one,
} from '@microsoft/rayfin-core';

import { Policy } from './Policy.js';

// A first-notice-of-loss claim raised against a policy. This is the operational
// record a claims-intake app captures; it lands in Fabric and later feeds the
// analytics estate (fact_claim) the BI labs report on.
@entity()
@authenticated('*')
export class Claim {
  @uuid() id!: string;
  @text({ max: 40 }) claimNumber!: string;
  @one(() => Policy) policy!: Policy;
  @set('Collision', 'Theft', 'Fire', 'Water Damage', 'Wind/Hail', 'Liability', 'Medical', 'Catastrophe')
  lossType!:
    | 'Collision' | 'Theft' | 'Fire' | 'Water Damage'
    | 'Wind/Hail' | 'Liability' | 'Medical' | 'Catastrophe';
  @set('Low', 'Medium', 'High', 'Severe')
  severity!: 'Low' | 'Medium' | 'High' | 'Severe';
  @set('Open', 'In Review', 'Approved', 'Paid', 'Denied', 'Closed')
  status!: 'Open' | 'In Review' | 'Approved' | 'Paid' | 'Denied' | 'Closed';
  @int() reserveAmount!: number;
  @int() paidAmount!: number;
  @date() lossDate!: Date;
  @date() reportedDate!: Date;
  @text({ max: 120, optional: true }) adjuster?: string;
  @date() createdAt!: Date;
}
