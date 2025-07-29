import { Lexer } from '../src/lexer';
import { Parser } from '../src/parser';
import { Transpiler } from '../src/transpiler';
import { TokenType } from '../src/types';

describe('DNA-Lang Compiler', () => {
  describe('Lexer', () => {
    test('tokenizes basic organism structure', () => {
      const source = `organism Test {
        dna { domain: "test" }
      }`;
      
      const lexer = new Lexer(source);
      const tokens = lexer.tokenize();
      
      expect(tokens[0].type).toBe(TokenType.ORGANISM);
      expect(tokens[1].type).toBe(TokenType.IDENTIFIER);
      expect(tokens[1].value).toBe('Test');
    });

    test('handles string literals', () => {
      const source = 'domain: "test-domain"';
      const lexer = new Lexer(source);
      const tokens = lexer.tokenize();
      
      expect(tokens[0].type).toBe(TokenType.IDENTIFIER);
      expect(tokens[1].type).toBe(TokenType.COLON);
      expect(tokens[2].type).toBe(TokenType.STRING);
      expect(tokens[2].value).toBe('test-domain');
    });

    test('handles arrays', () => {
      const source = 'participants: ["agent1", "agent2"]';
      const lexer = new Lexer(source);
      const tokens = lexer.tokenize();
      
      expect(tokens.some(t => t.type === TokenType.LBRACKET)).toBe(true);
      expect(tokens.some(t => t.type === TokenType.RBRACKET)).toBe(true);
    });
  });

  describe('Parser', () => {
    test('parses simple organism', () => {
      const source = `organism SimpleTest {
        dna {
          domain: "test"
          evolution_rate: "adaptive"
        }
        
        gene TestGene {
          purpose: "Testing"
          implementation: {
            code: "console.log('test')"
          }
        }
      }`;
      
      const lexer = new Lexer(source);
      const tokens = lexer.tokenize();
      const parser = new Parser(tokens);
      const ast = parser.parse();
      
      expect(ast.name).toBe('SimpleTest');
      expect(ast.dna.domain).toBe('test');
      expect(ast.dna.evolution_rate).toBe('adaptive');
      expect(ast.genes).toBeDefined();
      expect(ast.genes!.length).toBe(1);
      expect(ast.genes![0].name).toBe('TestGene');
      expect(ast.genes![0].purpose).toBe('Testing');
    });

    test('parses agents configuration', () => {
      const source = `organism TestOrg {
        dna { domain: "test" }
        
        agents {
          dev: DeveloperAgent(speed: fast)
          security: SecurityAgent(vigilance: high)
        }
      }`;
      
      const lexer = new Lexer(source);
      const tokens = lexer.tokenize();
      const parser = new Parser(tokens);
      const ast = parser.parse();
      
      expect(ast.agents).toBeDefined();
      expect(ast.agents!.length).toBe(2);
      expect(ast.agents![0].name).toBe('dev');
      expect(ast.agents![0].type).toBe('DeveloperAgent');
      expect(ast.agents![0].config.speed).toBe('fast');
    });
  });

  describe('Transpiler', () => {
    test('generates TypeScript class', () => {
      const organism = {
        name: 'TestOrganism',
        dna: {
          domain: 'test',
          evolution_rate: 'adaptive',
          immune_system: true
        },
        agents: [{
          name: 'testAgent',
          type: 'DeveloperAgent',
          config: { speed: 'fast' }
        }],
        genes: [{
          name: 'TestGene',
          purpose: 'Testing',
          implementation: {
            code: 'console.log("test")'
          }
        }]
      };
      
      const transpiler = new Transpiler();
      const typescript = transpiler.transpile(organism);
      
      expect(typescript).toContain('export class TestOrganism');
      expect(typescript).toContain('implements OrganismInterface');
      expect(typescript).toContain('public readonly dna: DNAConfig');
      expect(typescript).toContain('class DeveloperAgent');
      expect(typescript).toContain('async testgene()');
    });

    test('handles genome traits', () => {
      const organism = {
        name: 'TraitTest',
        dna: { domain: 'test' },
        genome: [
          { name: 'performance_optimized', value: 'always_active' },
          { name: 'secure', value: 'enabled' }
        ]
      };
      
      const transpiler = new Transpiler();
      const typescript = transpiler.transpile(organism);
      
      expect(typescript).toContain('performanceOptimized()');
      expect(typescript).toContain('secure()');
    });
  });

  describe('Integration', () => {
    test('compiles and generates valid TypeScript', () => {
      const source = `organism IntegrationTest {
        dna {
          domain: "integration"
          immune_system: enabled
        }
        
        agents {
          dev: DeveloperAgent(speed: normal)
        }
        
        gene SimpleFunction {
          implementation: {
            code: "function test() { return 'success'; }"
          }
        }
      }`;
      
      const lexer = new Lexer(source);
      const tokens = lexer.tokenize();
      const parser = new Parser(tokens);
      const ast = parser.parse();
      const transpiler = new Transpiler();
      const typescript = transpiler.transpile(ast);
      
      // Verify the generated TypeScript contains expected elements
      expect(typescript).toContain('export class IntegrationTest');
      expect(typescript).toContain('"domain": "integration"');
      expect(typescript).toContain('"immune_system": true');
      expect(typescript).toContain('DeveloperAgent');
      expect(typescript).toContain('function test() { return \'success\'; }');
    });
  });
});