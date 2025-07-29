import { Token, TokenType, OrganismDefinition, DNAConfig, AgentDefinition, GeneDefinition, TraitDefinition, CollaborationDefinition, EvolutionDefinition } from './types';

export class Parser {
  private tokens: Token[];
  private current: number = 0;

  constructor(tokens: Token[]) {
    this.tokens = tokens;
  }

  parse(): OrganismDefinition {
    this.skipNewlines();
    if (!this.check(TokenType.ORGANISM)) {
      throw new Error('Expected organism definition');
    }
    return this.parseOrganism();
  }

  private parseOrganism(): OrganismDefinition {
    this.consume(TokenType.ORGANISM, 'Expected "organism"');
    const name = this.consume(TokenType.IDENTIFIER, 'Expected organism name').value;
    this.consume(TokenType.LBRACE, 'Expected "{"');
    this.skipNewlines();

    const organism: OrganismDefinition = {
      name,
      dna: { domain: '' }
    };

    while (!this.check(TokenType.RBRACE) && !this.isAtEnd()) {
      this.skipNewlines();
      
      if (this.check(TokenType.DNA)) {
        organism.dna = this.parseDNA();
      } else if (this.check(TokenType.GENOME)) {
        organism.genome = this.parseGenome();
      } else if (this.check(TokenType.AGENTS)) {
        organism.agents = this.parseAgents();
      } else if (this.check(TokenType.GENE)) {
        if (!organism.genes) organism.genes = [];
        organism.genes.push(this.parseGene());
      } else if (this.check(TokenType.COLLABORATION)) {
        if (!organism.collaborations) organism.collaborations = [];
        organism.collaborations.push(this.parseCollaboration());
      } else if (this.check(TokenType.EVOLUTION)) {
        if (!organism.evolutions) organism.evolutions = [];
        organism.evolutions.push(this.parseEvolution());
      } else {
        throw new Error(`Unexpected token: ${this.peek().value} at line ${this.peek().line}`);
      }
      
      this.skipNewlines();
    }

    this.consume(TokenType.RBRACE, 'Expected "}"');
    return organism;
  }

  private parseDNA(): DNAConfig {
    this.consume(TokenType.DNA, 'Expected "dna"');
    this.consume(TokenType.LBRACE, 'Expected "{"');
    this.skipNewlines();

    const dna: DNAConfig = { domain: '' };

    while (!this.check(TokenType.RBRACE) && !this.isAtEnd()) {
      this.skipNewlines();
      
      // Allow keywords and identifiers for property names
      const token = this.peek();
      let key: string;
      if (token.type === TokenType.IDENTIFIER || Object.values(TokenType).includes(token.type as TokenType)) {
        key = this.advance().value;
      } else {
        throw new Error(`Expected property name, got ${token.type} at line ${token.line}`);
      }
      
      this.consume(TokenType.COLON, 'Expected ":"');
      const value = this.parseValue();

      switch (key) {
        case 'domain':
          dna.domain = value as string;
          break;
        case 'scale':
          dna.scale = value as string;
          break;
        case 'security_level':
          dna.security_level = value as string;
          break;
        case 'evolution_rate':
          dna.evolution_rate = value as string;
          break;
        case 'immune_system':
          dna.immune_system = value === 'enabled' || value === true;
          break;
      }

      this.skipNewlines();
    }

    this.consume(TokenType.RBRACE, 'Expected "}"');
    return dna;
  }

  private parseGenome(): TraitDefinition[] {
    this.consume(TokenType.GENOME, 'Expected "genome"');
    this.consume(TokenType.LBRACE, 'Expected "{"');
    this.skipNewlines();

    const traits: TraitDefinition[] = [];

    while (!this.check(TokenType.RBRACE) && !this.isAtEnd()) {
      this.skipNewlines();
      
      this.consume(TokenType.TRAIT, 'Expected "trait"');
      const name = this.consume(TokenType.IDENTIFIER, 'Expected trait name').value;
      this.consume(TokenType.COLON, 'Expected ":"');
      const value = this.parseValue() as string;

      traits.push({ name, value });
      this.skipNewlines();
    }

    this.consume(TokenType.RBRACE, 'Expected "}"');
    return traits;
  }

  private parseAgents(): AgentDefinition[] {
    this.consume(TokenType.AGENTS, 'Expected "agents"');
    this.consume(TokenType.LBRACE, 'Expected "{"');
    this.skipNewlines();

    const agents: AgentDefinition[] = [];

    while (!this.check(TokenType.RBRACE) && !this.isAtEnd()) {
      this.skipNewlines();
      
      const name = this.consume(TokenType.IDENTIFIER, 'Expected agent name').value;
      this.consume(TokenType.COLON, 'Expected ":"');
      const type = this.consume(TokenType.IDENTIFIER, 'Expected agent type').value;
      
      let config: Record<string, any> = {};
      if (this.check(TokenType.LPAREN)) {
        config = this.parseAgentConfig();
      }

      agents.push({ name, type, config });
      this.skipNewlines();
    }

    this.consume(TokenType.RBRACE, 'Expected "}"');
    return agents;
  }

  private parseAgentConfig(): Record<string, any> {
    this.consume(TokenType.LPAREN, 'Expected "("');
    const config: Record<string, any> = {};

    while (!this.check(TokenType.RPAREN) && !this.isAtEnd()) {
      const key = this.consume(TokenType.IDENTIFIER, 'Expected config key').value;
      this.consume(TokenType.COLON, 'Expected ":"');
      const value = this.parseValue();
      config[key] = value;

      if (this.check(TokenType.COMMA)) {
        this.advance();
      }
    }

    this.consume(TokenType.RPAREN, 'Expected ")"');
    return config;
  }

  private parseGene(): GeneDefinition {
    this.consume(TokenType.GENE, 'Expected "gene"');
    const name = this.consume(TokenType.IDENTIFIER, 'Expected gene name').value;
    this.consume(TokenType.LBRACE, 'Expected "{"');
    this.skipNewlines();

    const gene: GeneDefinition = { name, implementation: { code: '' } };

    while (!this.check(TokenType.RBRACE) && !this.isAtEnd()) {
      this.skipNewlines();
      
      // Allow both keywords and identifiers for property names
      let key: string;
      const token = this.peek();
      if (token.type === TokenType.IDENTIFIER || 
          token.type === TokenType.PURPOSE ||
          token.type === TokenType.IMPLEMENTATION ||
          token.type === TokenType.MUTATIONS ||
          token.type === TokenType.IMMUNE_RESPONSES) {
        key = this.advance().value;
      } else {
        throw new Error(`Expected property name, got ${token.type} at line ${token.line}`);
      }
      
      this.consume(TokenType.COLON, 'Expected ":"');

      switch (key) {
        case 'purpose':
          gene.purpose = this.parseValue() as string;
          break;
        case 'security_level':
          gene.security_level = this.parseValue() as string;
          break;
        case 'implementation':
          gene.implementation = this.parseImplementation();
          break;
        case 'mutations':
          gene.mutations = this.parseObjectLiteral();
          break;
        case 'immune_responses':
          gene.immune_responses = this.parseObjectLiteral();
          break;
        default:
          this.parseValue(); // Skip unknown properties
      }

      this.skipNewlines();
    }

    this.consume(TokenType.RBRACE, 'Expected "}"');
    return gene;
  }

  private parseImplementation(): { strategy?: string; code: string } {
    if (this.check(TokenType.LBRACE)) {
      this.advance();
      this.skipNewlines();
      
      const impl: { strategy?: string; code: string } = { code: '' };
      
      while (!this.check(TokenType.RBRACE) && !this.isAtEnd()) {
        this.skipNewlines();
        
        const token = this.peek();
        let key: string;
        if (token.type === TokenType.IDENTIFIER || Object.values(TokenType).includes(token.type as TokenType)) {
          key = this.advance().value;
        } else {
          throw new Error(`Expected property name, got ${token.type} at line ${token.line}`);
        }
        
        this.consume(TokenType.COLON, 'Expected ":"');
        const value = this.parseValue() as string;
        
        if (key === 'strategy') {
          impl.strategy = value;
        } else if (key === 'code') {
          impl.code = value;
        }
        
        // Handle optional comma
        if (this.check(TokenType.COMMA)) {
          this.advance();
        }
        
        this.skipNewlines();
      }
      
      this.consume(TokenType.RBRACE, 'Expected "}"');
      return impl;
    } else {
      const code = this.parseValue() as string;
      return { code };
    }
  }

  private parseCollaboration(): CollaborationDefinition {
    this.consume(TokenType.COLLABORATION, 'Expected "collaboration"');
    const name = this.consume(TokenType.IDENTIFIER, 'Expected collaboration name').value;
    this.consume(TokenType.LBRACE, 'Expected "{"');
    this.skipNewlines();

    const collaboration: CollaborationDefinition = {
      name,
      participants: [],
      workflow: []
    };

    while (!this.check(TokenType.RBRACE) && !this.isAtEnd()) {
      this.skipNewlines();
      
      const token = this.peek();
      let key: string;
      if (token.type === TokenType.IDENTIFIER || 
          token.type === TokenType.PARTICIPANTS ||
          token.type === TokenType.WORKFLOW ||
          Object.values(TokenType).includes(token.type as TokenType)) {
        key = this.advance().value;
      } else {
        throw new Error(`Expected property name, got ${token.type} at line ${token.line}`);
      }
      
      this.consume(TokenType.COLON, 'Expected ":"');

      switch (key) {
        case 'participants':
          collaboration.participants = this.parseStringArray();
          break;
        case 'workflow':
          collaboration.workflow = this.parseStringArray();
          break;
        case 'conflict_resolution':
          collaboration.conflict_resolution = this.parseObjectLiteral();
          break;
        default:
          this.parseValue(); // Skip unknown properties
      }

      this.skipNewlines();
    }

    this.consume(TokenType.RBRACE, 'Expected "}"');
    return collaboration;
  }

  private parseEvolution(): EvolutionDefinition {
    this.consume(TokenType.EVOLUTION, 'Expected "evolution"');
    const name = this.consume(TokenType.IDENTIFIER, 'Expected evolution name').value;
    this.consume(TokenType.LBRACE, 'Expected "{"');
    this.skipNewlines();

    const evolution: EvolutionDefinition = {
      name,
      trigger: '',
      mutations: {}
    };

    while (!this.check(TokenType.RBRACE) && !this.isAtEnd()) {
      this.skipNewlines();
      
      const token = this.peek();
      let key: string;
      if (token.type === TokenType.IDENTIFIER || 
          token.type === TokenType.TRIGGER ||
          token.type === TokenType.MUTATIONS ||
          Object.values(TokenType).includes(token.type as TokenType)) {
        key = this.advance().value;
      } else {
        throw new Error(`Expected property name, got ${token.type} at line ${token.line}`);
      }
      
      this.consume(TokenType.COLON, 'Expected ":"');

      switch (key) {
        case 'trigger':
          evolution.trigger = this.parseValue() as string;
          break;
        case 'mutations':
          evolution.mutations = this.parseObjectLiteral();
          break;
        case 'fitness_function':
          evolution.fitness_function = this.parseValue() as string;
          break;
        default:
          this.parseValue(); // Skip unknown properties
      }

      this.skipNewlines();
    }

    this.consume(TokenType.RBRACE, 'Expected "}"');
    return evolution;
  }

  private parseStringArray(): string[] {
    if (this.check(TokenType.LBRACKET)) {
      this.consume(TokenType.LBRACKET, 'Expected "["');
      const array: string[] = [];

      while (!this.check(TokenType.RBRACKET) && !this.isAtEnd()) {
        this.skipNewlines();
        const value = this.parseValue() as string;
        array.push(value);
        
        if (this.check(TokenType.COMMA)) {
          this.advance();
        }
        this.skipNewlines();
      }

      this.consume(TokenType.RBRACKET, 'Expected "]"');
      return array;
    } else {
      // Fallback to brace syntax for backward compatibility
      this.consume(TokenType.LBRACE, 'Expected "["');
      const array: string[] = [];

      while (!this.check(TokenType.RBRACE) && !this.isAtEnd()) {
        this.skipNewlines();
        const value = this.parseValue() as string;
        array.push(value);
        
        if (this.check(TokenType.COMMA)) {
          this.advance();
        }
        this.skipNewlines();
      }

      this.consume(TokenType.RBRACE, 'Expected "]"');
      return array;
    }
  }

  private parseObjectLiteral(): Record<string, any> {
    this.consume(TokenType.LBRACE, 'Expected "{"');
    this.skipNewlines();
    
    const obj: Record<string, any> = {};

    while (!this.check(TokenType.RBRACE) && !this.isAtEnd()) {
      this.skipNewlines();
      
      const token = this.peek();
      let key: string;
      if (token.type === TokenType.IDENTIFIER || Object.values(TokenType).includes(token.type as TokenType)) {
        key = this.advance().value;
      } else {
        throw new Error(`Expected property name, got ${token.type} at line ${token.line}`);
      }
      
      this.consume(TokenType.COLON, 'Expected ":"');
      const value = this.parseValue();
      obj[key] = value;

      // Handle optional comma
      if (this.check(TokenType.COMMA)) {
        this.advance();
      }
      this.skipNewlines();
    }

    this.consume(TokenType.RBRACE, 'Expected "}"');
    return obj;
  }

  private parseValue(): string | number | boolean {
    if (this.check(TokenType.STRING)) {
      return this.advance().value;
    } else if (this.check(TokenType.NUMBER)) {
      return parseFloat(this.advance().value);
    } else if (this.check(TokenType.IDENTIFIER)) {
      const value = this.advance().value;
      // Handle boolean-like identifiers
      if (value === 'true') return true;
      if (value === 'false') return false;
      if (value === 'enabled') return true;
      if (value === 'disabled') return false;
      return value;
    }
    
    throw new Error(`Expected value at line ${this.peek().line}`);
  }

  private skipNewlines(): void {
    while (this.check(TokenType.NEWLINE)) {
      this.advance();
    }
  }

  private consume(type: TokenType, message: string): Token {
    if (this.check(type)) {
      return this.advance();
    }
    
    throw new Error(`${message}. Got ${this.peek().type} at line ${this.peek().line}`);
  }

  private check(type: TokenType): boolean {
    if (this.isAtEnd()) return false;
    return this.peek().type === type;
  }

  private advance(): Token {
    if (!this.isAtEnd()) this.current++;
    return this.previous();
  }

  private isAtEnd(): boolean {
    return this.peek().type === TokenType.EOF;
  }

  private peek(): Token {
    return this.tokens[this.current];
  }

  private previous(): Token {
    return this.tokens[this.current - 1];
  }
}