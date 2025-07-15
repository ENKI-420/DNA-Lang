grammar dnaorganism;

// Lexer rules
DNAORGANISM  : 'dnaorganism';
DNAGENE      : 'dnagene';
DNA          : 'dna';
GENOME       : 'genome';
AGENTS       : 'agents';
IMMUNE_SYS   : 'dnaimmune_system';
MUTATIONS    : 'mutations';
ADAPTIVE_RES : 'adaptive_responses';
ID           : [a-zA-Z_][a-zA-Z_0-9]*;
STRING       : '"' (~["\\] | '\\' .)* '"';
NUMBER       : [0-9]+ ('.' [0-9]+)?;
LBRACE       : '{';
RBRACE       : '}';
LPAREN       : '(';
RPAREN       : ')';
SEMI         : ';';
COLON        : ':';
COMMA        : ',';
WS           : [ \t\r\n]+ -> skip;

// Parser rules
program           : organismDef* EOF;
organismDef       : DNAORGANISM ID LBRACE dnaBlock genomeBlock agentsBlock RBRACE;
dnaBlock          : DNA LBRACE attrPair* RBRACE;
genomeBlock       : GENOME LBRACE geneDef* RBRACE;
geneDef           : DNAGENE ID LBRACE geneBody RBRACE;
geneBody          : (attrPair | mutationsBlock | immuneBlock | adaptiveBlock)*;
mutationsBlock    : MUTATIONS LBRACE mutationDef* RBRACE;
mutationDef       : ID LBRACE attrPair* RBRACE;
immuneBlock       : IMMUNE_SYS LBRACE attrPair* RBRACE;
adaptiveBlock     : ADAPTIVE_RES LBRACE attrPair* RBRACE;
agentsBlock       : AGENTS LBRACE agentAssign* RBRACE;
agentAssign       : ID COLON ID SEMI;
attrPair          : ID COLON (STRING | NUMBER) SEMI;