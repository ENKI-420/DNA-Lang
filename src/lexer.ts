import { Token, TokenType } from './types';

export class Lexer {
  private source: string;
  private position: number = 0;
  private line: number = 1;
  private column: number = 1;

  constructor(source: string) {
    this.source = source;
  }

  tokenize(): Token[] {
    const tokens: Token[] = [];
    
    while (this.position < this.source.length) {
      const token = this.nextToken();
      if (token) {
        tokens.push(token);
      }
    }
    
    tokens.push({
      type: TokenType.EOF,
      value: '',
      line: this.line,
      column: this.column
    });
    
    return tokens;
  }

  private nextToken(): Token | null {
    this.skipWhitespace();
    
    if (this.position >= this.source.length) {
      return null;
    }

    const start = this.position;
    const startLine = this.line;
    const startColumn = this.column;

    const char = this.source[this.position];

    // Handle newlines
    if (char === '\n') {
      this.advance();
      return {
        type: TokenType.NEWLINE,
        value: '\n',
        line: startLine,
        column: startColumn
      };
    }

    // Handle comments
    if (char === '/' && this.peek() === '/') {
      this.skipLineComment();
      return this.nextToken();
    }

    // Handle strings
    if (char === '"' || char === "'") {
      return this.readString(char);
    }

    // Handle numbers
    if (this.isDigit(char)) {
      return this.readNumber();
    }

    // Handle identifiers and keywords
    if (this.isAlpha(char) || char === '_') {
      return this.readIdentifier();
    }

    // Handle single character tokens
    switch (char) {
      case '{':
        this.advance();
        return { type: TokenType.LBRACE, value: '{', line: startLine, column: startColumn };
      case '}':
        this.advance();
        return { type: TokenType.RBRACE, value: '}', line: startLine, column: startColumn };
      case '(':
        this.advance();
        return { type: TokenType.LPAREN, value: '(', line: startLine, column: startColumn };
      case ')':
        this.advance();
        return { type: TokenType.RPAREN, value: ')', line: startLine, column: startColumn };
      case '[':
        this.advance();
        return { type: TokenType.LBRACKET, value: '[', line: startLine, column: startColumn };
      case ']':
        this.advance();
        return { type: TokenType.RBRACKET, value: ']', line: startLine, column: startColumn };
      case ':':
        this.advance();
        return { type: TokenType.COLON, value: ':', line: startLine, column: startColumn };
      case ',':
        this.advance();
        return { type: TokenType.COMMA, value: ',', line: startLine, column: startColumn };
      default:
        throw new Error(`Unexpected character '${char}' at line ${this.line}, column ${this.column}`);
    }
  }

  private advance(): void {
    if (this.position < this.source.length) {
      if (this.source[this.position] === '\n') {
        this.line++;
        this.column = 1;
      } else {
        this.column++;
      }
      this.position++;
    }
  }

  private peek(): string {
    if (this.position + 1 >= this.source.length) {
      return '\0';
    }
    return this.source[this.position + 1];
  }

  private skipWhitespace(): void {
    while (this.position < this.source.length) {
      const char = this.source[this.position];
      if (char === ' ' || char === '\t' || char === '\r') {
        this.advance();
      } else {
        break;
      }
    }
  }

  private skipLineComment(): void {
    while (this.position < this.source.length && this.source[this.position] !== '\n') {
      this.advance();
    }
  }

  private readString(quote: string): Token {
    const startLine = this.line;
    const startColumn = this.column;
    let value = '';
    
    this.advance(); // Skip opening quote
    
    while (this.position < this.source.length && this.source[this.position] !== quote) {
      if (this.source[this.position] === '\\') {
        this.advance();
        if (this.position < this.source.length) {
          value += this.source[this.position];
          this.advance();
        }
      } else {
        value += this.source[this.position];
        this.advance();
      }
    }
    
    if (this.position >= this.source.length) {
      throw new Error(`Unterminated string at line ${startLine}, column ${startColumn}`);
    }
    
    this.advance(); // Skip closing quote
    
    return {
      type: TokenType.STRING,
      value,
      line: startLine,
      column: startColumn
    };
  }

  private readNumber(): Token {
    const startLine = this.line;
    const startColumn = this.column;
    let value = '';
    
    while (this.position < this.source.length && (this.isDigit(this.source[this.position]) || this.source[this.position] === '.')) {
      value += this.source[this.position];
      this.advance();
    }
    
    return {
      type: TokenType.NUMBER,
      value,
      line: startLine,
      column: startColumn
    };
  }

  private readIdentifier(): Token {
    const startLine = this.line;
    const startColumn = this.column;
    let value = '';
    
    while (this.position < this.source.length && (this.isAlphaNumeric(this.source[this.position]) || this.source[this.position] === '_')) {
      value += this.source[this.position];
      this.advance();
    }
    
    const tokenType = this.getKeywordType(value) || TokenType.IDENTIFIER;
    
    return {
      type: tokenType,
      value,
      line: startLine,
      column: startColumn
    };
  }

  private getKeywordType(value: string): TokenType | null {
    const keywords: Record<string, TokenType> = {
      'organism': TokenType.ORGANISM,
      'dna': TokenType.DNA,
      'genome': TokenType.GENOME,
      'agents': TokenType.AGENTS,
      'gene': TokenType.GENE,
      'collaboration': TokenType.COLLABORATION,
      'evolution': TokenType.EVOLUTION,
      'trait': TokenType.TRAIT,
      'purpose': TokenType.PURPOSE,
      'implementation': TokenType.IMPLEMENTATION,
      'mutations': TokenType.MUTATIONS,
      'immune_responses': TokenType.IMMUNE_RESPONSES,
      'participants': TokenType.PARTICIPANTS,
      'workflow': TokenType.WORKFLOW,
      'trigger': TokenType.TRIGGER
    };
    
    return keywords[value] || null;
  }

  private isDigit(char: string): boolean {
    return char >= '0' && char <= '9';
  }

  private isAlpha(char: string): boolean {
    return (char >= 'a' && char <= 'z') || (char >= 'A' && char <= 'Z');
  }

  private isAlphaNumeric(char: string): boolean {
    return this.isAlpha(char) || this.isDigit(char);
  }
}