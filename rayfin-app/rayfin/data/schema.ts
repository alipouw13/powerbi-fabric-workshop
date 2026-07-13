import { Customer } from './Customer.js';
import { Agent } from './Agent.js';
import { Policy } from './Policy.js';
import { Claim } from './Claim.js';

export type InsuranceSchema = {
  Customer: Customer;
  Agent: Agent;
  Policy: Policy;
  Claim: Claim;
};

export const schema = [Customer, Agent, Policy, Claim];
