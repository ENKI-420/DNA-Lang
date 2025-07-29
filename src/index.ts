// DNA-Lang: The Genetic Programming Language Framework
// Main entry point for the DNA-Lang compiler and runtime

export { Lexer } from './lexer';
export { Parser } from './parser';
export { Transpiler } from './transpiler';
export * from './types';

// Compiler API
export async function compileSource(source: string): Promise<string> {
  const { Lexer } = await import('./lexer');
  const { Parser } = await import('./parser');
  const { Transpiler } = await import('./transpiler');
  
  const lexer = new Lexer(source);
  const tokens = lexer.tokenize();
  
  const parser = new Parser(tokens);
  const ast = parser.parse();
  
  const transpiler = new Transpiler();
  return transpiler.transpile(ast);
}

export async function compileFile(filePath: string): Promise<string> {
  const fs = await import('fs');
  const source = fs.readFileSync(filePath, 'utf-8');
  return compileSource(source);
}