// DNA-Lang Type Definitions

export interface DNAConfig {
  domain: string;
  scale?: string;
  security_level?: string;
  evolution_rate?: string;
  immune_system?: boolean;
}

export interface TraitDefinition {
  name: string;
  value: string;
}

export interface AgentDefinition {
  name: string;
  type: string;
  config: Record<string, any>;
}

export interface GeneDefinition {
  name: string;
  purpose?: string;
  security_level?: string;
  implementation?: {
    strategy?: string;
    code: string;
  };
  mutations?: Record<string, string>;
  immune_responses?: Record<string, string>;
}

export interface CollaborationDefinition {
  name: string;
  participants: string[];
  workflow: string[];
  conflict_resolution?: Record<string, string>;
}

export interface EvolutionDefinition {
  name: string;
  trigger: string;
  mutations: Record<string, any>;
  fitness_function?: string;
}

export interface OrganismDefinition {
  name: string;
  dna: DNAConfig;
  genome?: TraitDefinition[];
  agents?: AgentDefinition[];
  genes?: GeneDefinition[];
  collaborations?: CollaborationDefinition[];
  evolutions?: EvolutionDefinition[];
}

export interface Token {
  type: TokenType;
  value: string;
  line: number;
  column: number;
}

export enum TokenType {
  ORGANISM = 'ORGANISM',
  DNA = 'DNA',
  GENOME = 'GENOME', 
  AGENTS = 'AGENTS',
  GENE = 'GENE',
  COLLABORATION = 'COLLABORATION',
  EVOLUTION = 'EVOLUTION',
  IDENTIFIER = 'IDENTIFIER',
  STRING = 'STRING',
  NUMBER = 'NUMBER',
  COLON = 'COLON',
  COMMA = 'COMMA',
  LBRACE = 'LBRACE',
  RBRACE = 'RBRACE',
  LPAREN = 'LPAREN',
  RPAREN = 'RPAREN',
  LBRACKET = 'LBRACKET',
  RBRACKET = 'RBRACKET',
  NEWLINE = 'NEWLINE',
  EOF = 'EOF',
  TRAIT = 'TRAIT',
  PURPOSE = 'PURPOSE',
  IMPLEMENTATION = 'IMPLEMENTATION',
  MUTATIONS = 'MUTATIONS',
  IMMUNE_RESPONSES = 'IMMUNE_RESPONSES',
  PARTICIPANTS = 'PARTICIPANTS',
  WORKFLOW = 'WORKFLOW',
  TRIGGER = 'TRIGGER'
}

export interface ASTNode {
  type: string;
  [key: string]: any;
}

export interface OrganismInterface {
  dna: DNAConfig;
  agents?: Map<string, AgentInterface>;
  evolve(): Promise<void>;
  selfHeal(): Promise<void>;
}

export interface AgentInterface {
  name: string;
  type: string;
  execute(task: string): Promise<any>;
}