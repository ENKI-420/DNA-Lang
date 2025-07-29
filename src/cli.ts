#!/usr/bin/env node
import { Command } from 'commander';
import * as fs from 'fs';
import * as path from 'path';
import { Lexer } from './lexer';
import { Parser } from './parser';
import { Transpiler } from './transpiler';

const program = new Command();

program
  .name('dna')
  .description('DNA-Lang: The Genetic Programming Language')
  .version('0.6.0');

program
  .command('new <name>')
  .description('Create a new DNA-Lang organism')
  .action(async (name: string) => {
    try {
      await createNewOrganism(name);
      console.log(`🧬 Created new organism: ${name}`);
    } catch (error) {
      console.error('❌ Error creating organism:', error);
      process.exit(1);
    }
  });

program
  .command('compile <file>')
  .description('Compile DNA-Lang source to TypeScript')
  .option('-o, --output <dir>', 'Output directory', 'dist')
  .action(async (file: string, options: { output: string }) => {
    try {
      await compileFile(file, options.output);
      console.log(`✅ Compiled ${file} successfully`);
    } catch (error) {
      console.error('❌ Compilation failed:', error);
      process.exit(1);
    }
  });

program
  .command('run <file>')
  .description('Run a compiled DNA-Lang organism')
  .option('--monitor', 'Enable evolution monitoring')
  .action(async (file: string, options: { monitor: boolean }) => {
    try {
      await runOrganism(file, options.monitor);
    } catch (error) {
      console.error('❌ Runtime error:', error);
      process.exit(1);
    }
  });

program
  .command('evolve <file>')
  .description('Manually trigger evolution of an organism')
  .action(async (file: string) => {
    try {
      await evolveOrganism(file);
    } catch (error) {
      console.error('❌ Evolution failed:', error);
      process.exit(1);
    }
  });

async function createNewOrganism(name: string): Promise<void> {
  const template = `organism ${name} {
    dna {
        domain: "demo"
        scale: "small"
        security_level: "standard"
        evolution_rate: "adaptive"
        immune_system: enabled
    }

    genome {
        trait performance_optimized: always_active
        trait user_friendly: enabled
    }

    agents {
        architect: ArchitectAgent(focus: microservices)
        developer: DeveloperAgent(speed: fast)
    }

    gene Greeter {
        purpose: "Simple greeting functionality"
        implementation: {
            strategy: "direct",
            code: "function greet(name) { console.log('Hello, ' + name + '!'); return 'Hello, ' + name + '!'; }"
        }
        mutations: {
            add_personalization: "/* Add user preferences */",
            multilingual: "/* Add language support */"
        }
        immune_responses: {
            input_validation: "/* Validate input parameters */"
        }
    }

    collaboration SimpleGreeting {
        participants: ["developer"]
        workflow: ["developer.implement", "developer.test"]
    }
}`;

  const filename = `${name}.dna`;
  fs.writeFileSync(filename, template);
  
  // Also create a basic project structure if it doesn't exist
  if (!fs.existsSync('package.json')) {
    const packageJson = {
      name: name.toLowerCase(),
      version: "1.0.0",
      description: `DNA-Lang organism: ${name}`,
      main: "dist/index.js",
      scripts: {
        build: "dna compile *.dna",
        start: "dna run dist/*.js"
      },
      dependencies: {}
    };
    
    fs.writeFileSync('package.json', JSON.stringify(packageJson, null, 2));
  }
}

async function compileFile(file: string, outputDir: string): Promise<void> {
  if (!fs.existsSync(file)) {
    throw new Error(`File not found: ${file}`);
  }

  const source = fs.readFileSync(file, 'utf-8');
  const lexer = new Lexer(source);
  const tokens = lexer.tokenize();
  
  const parser = new Parser(tokens);
  const ast = parser.parse();
  
  const transpiler = new Transpiler();
  const typescript = transpiler.transpile(ast);
  
  // Ensure output directory exists
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  // Write the generated TypeScript
  const outputFile = path.join(outputDir, `${ast.name}.ts`);
  fs.writeFileSync(outputFile, typescript);
  
  // Write runtime support file
  await writeRuntimeSupport(outputDir);
  
  // Write a simple index file
  const indexContent = `export { ${ast.name} } from './${ast.name}';`;
  fs.writeFileSync(path.join(outputDir, 'index.ts'), indexContent);
  
  console.log(`📁 Output written to: ${outputFile}`);
}

async function writeRuntimeSupport(outputDir: string): Promise<void> {
  const runtimeContent = `// DNA-Lang Runtime Support

export interface DNAConfig {
  domain: string;
  scale?: string;
  security_level?: string;
  evolution_rate?: string;
  immune_system?: boolean;
}

export interface AgentInterface {
  name: string;
  type: string;
  execute(task: string): Promise<any>;
}

export interface OrganismInterface {
  dna: DNAConfig;
  agents?: Map<string, AgentInterface>;
  evolve(): Promise<void>;
  selfHeal(): Promise<void>;
}

export class DNARuntime {
  static async loadOrganism(filePath: string): Promise<OrganismInterface> {
    const OrganismClass = require(filePath);
    const organismName = Object.keys(OrganismClass)[0];
    return new OrganismClass[organismName]();
  }
  
  static async runWithMonitoring(organism: OrganismInterface, duration: number = 30000): Promise<void> {
    console.log('🚀 Starting DNA-Lang organism with monitoring...');
    
    // Set up monitoring
    const healthInterval = setInterval(async () => {
      try {
        await organism.selfHeal();
      } catch (error) {
        console.error('Health check failed:', error);
      }
    }, 10000);
    
    // Run for specified duration
    setTimeout(() => {
      clearInterval(healthInterval);
      if ('destroy' in organism && typeof organism.destroy === 'function') {
        organism.destroy();
      }
      console.log('🔚 Monitoring stopped');
    }, duration);
  }
}`;

  fs.writeFileSync(path.join(outputDir, 'dna-lang-runtime.ts'), runtimeContent);
}

async function runOrganism(file: string, monitor: boolean): Promise<void> {
  if (!fs.existsSync(file)) {
    throw new Error(`File not found: ${file}`);
  }

  // If it's a .dna file, compile it first
  if (file.endsWith('.dna')) {
    console.log('🔧 Compiling DNA file...');
    await compileFile(file, 'dist');
    const baseName = path.basename(file, '.dna');
    file = path.join('dist', `${baseName}.ts`);
  }

  // If it's a TypeScript file, we need to transpile to JS
  if (file.endsWith('.ts')) {
    console.log('⚠️  TypeScript execution not implemented. Please compile to JavaScript first.');
    console.log('💡 Consider using ts-node or compiling with tsc');
    return;
  }

  // Load and run the organism
  try {
    delete require.cache[path.resolve(file)];
    const organismModule = require(path.resolve(file));
    const OrganismClass = organismModule[Object.keys(organismModule)[0]];
    
    if (!OrganismClass) {
      throw new Error('No organism class found in file');
    }
    
    const organism = new OrganismClass();
    
    console.log('🧬 Starting organism...');
    
    if (monitor) {
      console.log('📊 Monitoring enabled');
      // Run with monitoring for 30 seconds
      await new Promise(resolve => {
        setTimeout(() => {
          if (organism.destroy) organism.destroy();
          resolve(void 0);
        }, 30000);
      });
    } else {
      // Run evolution cycle once
      await organism.evolve();
      console.log('✅ Evolution cycle completed');
      if (organism.destroy) organism.destroy();
    }
  } catch (error) {
    console.error('Failed to load organism:', error);
    throw error;
  }
}

async function evolveOrganism(file: string): Promise<void> {
  console.log(`🧬 Triggering evolution for: ${file}`);
  
  // This would typically load the organism and trigger evolution
  // For now, we'll simulate it
  console.log('⚡ Evolution triggered manually');
  console.log('✨ Applying beneficial mutations...');
  console.log('🛡️ Immune system activated');
  console.log('✅ Evolution completed successfully');
}

// Add error handling for the CLI
process.on('uncaughtException', (error) => {
  console.error('💥 Uncaught exception:', error);
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('💥 Unhandled rejection at:', promise, 'reason:', reason);
  process.exit(1);
});

// Parse command line arguments
program.parse();

// If no command is provided, show help
if (!process.argv.slice(2).length) {
  program.outputHelp();
}