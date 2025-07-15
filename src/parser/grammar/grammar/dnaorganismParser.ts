// Generated from grammar/dnaorganism.g4 by ANTLR 4.9.0-SNAPSHOT


import { ATN } from "antlr4ts/atn/ATN";
import { ATNDeserializer } from "antlr4ts/atn/ATNDeserializer";
import { FailedPredicateException } from "antlr4ts/FailedPredicateException";
import { NotNull } from "antlr4ts/Decorators";
import { NoViableAltException } from "antlr4ts/NoViableAltException";
import { Override } from "antlr4ts/Decorators";
import { Parser } from "antlr4ts/Parser";
import { ParserRuleContext } from "antlr4ts/ParserRuleContext";
import { ParserATNSimulator } from "antlr4ts/atn/ParserATNSimulator";
import { ParseTreeListener } from "antlr4ts/tree/ParseTreeListener";
import { ParseTreeVisitor } from "antlr4ts/tree/ParseTreeVisitor";
import { RecognitionException } from "antlr4ts/RecognitionException";
import { RuleContext } from "antlr4ts/RuleContext";
//import { RuleVersion } from "antlr4ts/RuleVersion";
import { TerminalNode } from "antlr4ts/tree/TerminalNode";
import { Token } from "antlr4ts/Token";
import { TokenStream } from "antlr4ts/TokenStream";
import { Vocabulary } from "antlr4ts/Vocabulary";
import { VocabularyImpl } from "antlr4ts/VocabularyImpl";

import * as Utils from "antlr4ts/misc/Utils";

import { dnaorganismListener } from "./dnaorganismListener";
import { dnaorganismVisitor } from "./dnaorganismVisitor";


export class dnaorganismParser extends Parser {
	public static readonly DNAORGANISM = 1;
	public static readonly DNAGENE = 2;
	public static readonly DNA = 3;
	public static readonly GENOME = 4;
	public static readonly AGENTS = 5;
	public static readonly IMMUNE_SYS = 6;
	public static readonly MUTATIONS = 7;
	public static readonly ADAPTIVE_RES = 8;
	public static readonly ID = 9;
	public static readonly STRING = 10;
	public static readonly NUMBER = 11;
	public static readonly LBRACE = 12;
	public static readonly RBRACE = 13;
	public static readonly LPAREN = 14;
	public static readonly RPAREN = 15;
	public static readonly SEMI = 16;
	public static readonly COLON = 17;
	public static readonly COMMA = 18;
	public static readonly WS = 19;
	public static readonly RULE_program = 0;
	public static readonly RULE_organismDef = 1;
	public static readonly RULE_dnaBlock = 2;
	public static readonly RULE_genomeBlock = 3;
	public static readonly RULE_geneDef = 4;
	public static readonly RULE_geneBody = 5;
	public static readonly RULE_mutationsBlock = 6;
	public static readonly RULE_mutationDef = 7;
	public static readonly RULE_immuneBlock = 8;
	public static readonly RULE_adaptiveBlock = 9;
	public static readonly RULE_agentsBlock = 10;
	public static readonly RULE_agentAssign = 11;
	public static readonly RULE_attrPair = 12;
	// tslint:disable:no-trailing-whitespace
	public static readonly ruleNames: string[] = [
		"program", "organismDef", "dnaBlock", "genomeBlock", "geneDef", "geneBody", 
		"mutationsBlock", "mutationDef", "immuneBlock", "adaptiveBlock", "agentsBlock", 
		"agentAssign", "attrPair",
	];

	private static readonly _LITERAL_NAMES: Array<string | undefined> = [
		undefined, "'dnaorganism'", "'dnagene'", "'dna'", "'genome'", "'agents'", 
		"'dnaimmune_system'", "'mutations'", "'adaptive_responses'", undefined, 
		undefined, undefined, "'{'", "'}'", "'('", "')'", "';'", "':'", "','",
	];
	private static readonly _SYMBOLIC_NAMES: Array<string | undefined> = [
		undefined, "DNAORGANISM", "DNAGENE", "DNA", "GENOME", "AGENTS", "IMMUNE_SYS", 
		"MUTATIONS", "ADAPTIVE_RES", "ID", "STRING", "NUMBER", "LBRACE", "RBRACE", 
		"LPAREN", "RPAREN", "SEMI", "COLON", "COMMA", "WS",
	];
	public static readonly VOCABULARY: Vocabulary = new VocabularyImpl(dnaorganismParser._LITERAL_NAMES, dnaorganismParser._SYMBOLIC_NAMES, []);

	// @Override
	// @NotNull
	public get vocabulary(): Vocabulary {
		return dnaorganismParser.VOCABULARY;
	}
	// tslint:enable:no-trailing-whitespace

	// @Override
	public get grammarFileName(): string { return "dnaorganism.g4"; }

	// @Override
	public get ruleNames(): string[] { return dnaorganismParser.ruleNames; }

	// @Override
	public get serializedATN(): string { return dnaorganismParser._serializedATN; }

	protected createFailedPredicateException(predicate?: string, message?: string): FailedPredicateException {
		return new FailedPredicateException(this, predicate, message);
	}

	constructor(input: TokenStream) {
		super(input);
		this._interp = new ParserATNSimulator(dnaorganismParser._ATN, this);
	}
	// @RuleVersion(0)
	public program(): ProgramContext {
		let _localctx: ProgramContext = new ProgramContext(this._ctx, this.state);
		this.enterRule(_localctx, 0, dnaorganismParser.RULE_program);
		let _la: number;
		try {
			this.enterOuterAlt(_localctx, 1);
			{
			this.state = 29;
			this._errHandler.sync(this);
			_la = this._input.LA(1);
			while (_la === dnaorganismParser.DNAORGANISM) {
				{
				{
				this.state = 26;
				this.organismDef();
				}
				}
				this.state = 31;
				this._errHandler.sync(this);
				_la = this._input.LA(1);
			}
			this.state = 32;
			this.match(dnaorganismParser.EOF);
			}
		}
		catch (re) {
			if (re instanceof RecognitionException) {
				_localctx.exception = re;
				this._errHandler.reportError(this, re);
				this._errHandler.recover(this, re);
			} else {
				throw re;
			}
		}
		finally {
			this.exitRule();
		}
		return _localctx;
	}
	// @RuleVersion(0)
	public organismDef(): OrganismDefContext {
		let _localctx: OrganismDefContext = new OrganismDefContext(this._ctx, this.state);
		this.enterRule(_localctx, 2, dnaorganismParser.RULE_organismDef);
		try {
			this.enterOuterAlt(_localctx, 1);
			{
			this.state = 34;
			this.match(dnaorganismParser.DNAORGANISM);
			this.state = 35;
			this.match(dnaorganismParser.ID);
			this.state = 36;
			this.match(dnaorganismParser.LBRACE);
			this.state = 37;
			this.dnaBlock();
			this.state = 38;
			this.genomeBlock();
			this.state = 39;
			this.agentsBlock();
			this.state = 40;
			this.match(dnaorganismParser.RBRACE);
			}
		}
		catch (re) {
			if (re instanceof RecognitionException) {
				_localctx.exception = re;
				this._errHandler.reportError(this, re);
				this._errHandler.recover(this, re);
			} else {
				throw re;
			}
		}
		finally {
			this.exitRule();
		}
		return _localctx;
	}
	// @RuleVersion(0)
	public dnaBlock(): DnaBlockContext {
		let _localctx: DnaBlockContext = new DnaBlockContext(this._ctx, this.state);
		this.enterRule(_localctx, 4, dnaorganismParser.RULE_dnaBlock);
		let _la: number;
		try {
			this.enterOuterAlt(_localctx, 1);
			{
			this.state = 42;
			this.match(dnaorganismParser.DNA);
			this.state = 43;
			this.match(dnaorganismParser.LBRACE);
			this.state = 47;
			this._errHandler.sync(this);
			_la = this._input.LA(1);
			while (_la === dnaorganismParser.ID) {
				{
				{
				this.state = 44;
				this.attrPair();
				}
				}
				this.state = 49;
				this._errHandler.sync(this);
				_la = this._input.LA(1);
			}
			this.state = 50;
			this.match(dnaorganismParser.RBRACE);
			}
		}
		catch (re) {
			if (re instanceof RecognitionException) {
				_localctx.exception = re;
				this._errHandler.reportError(this, re);
				this._errHandler.recover(this, re);
			} else {
				throw re;
			}
		}
		finally {
			this.exitRule();
		}
		return _localctx;
	}
	// @RuleVersion(0)
	public genomeBlock(): GenomeBlockContext {
		let _localctx: GenomeBlockContext = new GenomeBlockContext(this._ctx, this.state);
		this.enterRule(_localctx, 6, dnaorganismParser.RULE_genomeBlock);
		let _la: number;
		try {
			this.enterOuterAlt(_localctx, 1);
			{
			this.state = 52;
			this.match(dnaorganismParser.GENOME);
			this.state = 53;
			this.match(dnaorganismParser.LBRACE);
			this.state = 57;
			this._errHandler.sync(this);
			_la = this._input.LA(1);
			while (_la === dnaorganismParser.DNAGENE) {
				{
				{
				this.state = 54;
				this.geneDef();
				}
				}
				this.state = 59;
				this._errHandler.sync(this);
				_la = this._input.LA(1);
			}
			this.state = 60;
			this.match(dnaorganismParser.RBRACE);
			}
		}
		catch (re) {
			if (re instanceof RecognitionException) {
				_localctx.exception = re;
				this._errHandler.reportError(this, re);
				this._errHandler.recover(this, re);
			} else {
				throw re;
			}
		}
		finally {
			this.exitRule();
		}
		return _localctx;
	}
	// @RuleVersion(0)
	public geneDef(): GeneDefContext {
		let _localctx: GeneDefContext = new GeneDefContext(this._ctx, this.state);
		this.enterRule(_localctx, 8, dnaorganismParser.RULE_geneDef);
		try {
			this.enterOuterAlt(_localctx, 1);
			{
			this.state = 62;
			this.match(dnaorganismParser.DNAGENE);
			this.state = 63;
			this.match(dnaorganismParser.ID);
			this.state = 64;
			this.match(dnaorganismParser.LBRACE);
			this.state = 65;
			this.geneBody();
			this.state = 66;
			this.match(dnaorganismParser.RBRACE);
			}
		}
		catch (re) {
			if (re instanceof RecognitionException) {
				_localctx.exception = re;
				this._errHandler.reportError(this, re);
				this._errHandler.recover(this, re);
			} else {
				throw re;
			}
		}
		finally {
			this.exitRule();
		}
		return _localctx;
	}
	// @RuleVersion(0)
	public geneBody(): GeneBodyContext {
		let _localctx: GeneBodyContext = new GeneBodyContext(this._ctx, this.state);
		this.enterRule(_localctx, 10, dnaorganismParser.RULE_geneBody);
		let _la: number;
		try {
			this.enterOuterAlt(_localctx, 1);
			{
			this.state = 74;
			this._errHandler.sync(this);
			_la = this._input.LA(1);
			while ((((_la) & ~0x1F) === 0 && ((1 << _la) & ((1 << dnaorganismParser.IMMUNE_SYS) | (1 << dnaorganismParser.MUTATIONS) | (1 << dnaorganismParser.ADAPTIVE_RES) | (1 << dnaorganismParser.ID))) !== 0)) {
				{
				this.state = 72;
				this._errHandler.sync(this);
				switch (this._input.LA(1)) {
				case dnaorganismParser.ID:
					{
					this.state = 68;
					this.attrPair();
					}
					break;
				case dnaorganismParser.MUTATIONS:
					{
					this.state = 69;
					this.mutationsBlock();
					}
					break;
				case dnaorganismParser.IMMUNE_SYS:
					{
					this.state = 70;
					this.immuneBlock();
					}
					break;
				case dnaorganismParser.ADAPTIVE_RES:
					{
					this.state = 71;
					this.adaptiveBlock();
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				}
				this.state = 76;
				this._errHandler.sync(this);
				_la = this._input.LA(1);
			}
			}
		}
		catch (re) {
			if (re instanceof RecognitionException) {
				_localctx.exception = re;
				this._errHandler.reportError(this, re);
				this._errHandler.recover(this, re);
			} else {
				throw re;
			}
		}
		finally {
			this.exitRule();
		}
		return _localctx;
	}
	// @RuleVersion(0)
	public mutationsBlock(): MutationsBlockContext {
		let _localctx: MutationsBlockContext = new MutationsBlockContext(this._ctx, this.state);
		this.enterRule(_localctx, 12, dnaorganismParser.RULE_mutationsBlock);
		let _la: number;
		try {
			this.enterOuterAlt(_localctx, 1);
			{
			this.state = 77;
			this.match(dnaorganismParser.MUTATIONS);
			this.state = 78;
			this.match(dnaorganismParser.LBRACE);
			this.state = 82;
			this._errHandler.sync(this);
			_la = this._input.LA(1);
			while (_la === dnaorganismParser.ID) {
				{
				{
				this.state = 79;
				this.mutationDef();
				}
				}
				this.state = 84;
				this._errHandler.sync(this);
				_la = this._input.LA(1);
			}
			this.state = 85;
			this.match(dnaorganismParser.RBRACE);
			}
		}
		catch (re) {
			if (re instanceof RecognitionException) {
				_localctx.exception = re;
				this._errHandler.reportError(this, re);
				this._errHandler.recover(this, re);
			} else {
				throw re;
			}
		}
		finally {
			this.exitRule();
		}
		return _localctx;
	}
	// @RuleVersion(0)
	public mutationDef(): MutationDefContext {
		let _localctx: MutationDefContext = new MutationDefContext(this._ctx, this.state);
		this.enterRule(_localctx, 14, dnaorganismParser.RULE_mutationDef);
		let _la: number;
		try {
			this.enterOuterAlt(_localctx, 1);
			{
			this.state = 87;
			this.match(dnaorganismParser.ID);
			this.state = 88;
			this.match(dnaorganismParser.LBRACE);
			this.state = 92;
			this._errHandler.sync(this);
			_la = this._input.LA(1);
			while (_la === dnaorganismParser.ID) {
				{
				{
				this.state = 89;
				this.attrPair();
				}
				}
				this.state = 94;
				this._errHandler.sync(this);
				_la = this._input.LA(1);
			}
			this.state = 95;
			this.match(dnaorganismParser.RBRACE);
			}
		}
		catch (re) {
			if (re instanceof RecognitionException) {
				_localctx.exception = re;
				this._errHandler.reportError(this, re);
				this._errHandler.recover(this, re);
			} else {
				throw re;
			}
		}
		finally {
			this.exitRule();
		}
		return _localctx;
	}
	// @RuleVersion(0)
	public immuneBlock(): ImmuneBlockContext {
		let _localctx: ImmuneBlockContext = new ImmuneBlockContext(this._ctx, this.state);
		this.enterRule(_localctx, 16, dnaorganismParser.RULE_immuneBlock);
		let _la: number;
		try {
			this.enterOuterAlt(_localctx, 1);
			{
			this.state = 97;
			this.match(dnaorganismParser.IMMUNE_SYS);
			this.state = 98;
			this.match(dnaorganismParser.LBRACE);
			this.state = 102;
			this._errHandler.sync(this);
			_la = this._input.LA(1);
			while (_la === dnaorganismParser.ID) {
				{
				{
				this.state = 99;
				this.attrPair();
				}
				}
				this.state = 104;
				this._errHandler.sync(this);
				_la = this._input.LA(1);
			}
			this.state = 105;
			this.match(dnaorganismParser.RBRACE);
			}
		}
		catch (re) {
			if (re instanceof RecognitionException) {
				_localctx.exception = re;
				this._errHandler.reportError(this, re);
				this._errHandler.recover(this, re);
			} else {
				throw re;
			}
		}
		finally {
			this.exitRule();
		}
		return _localctx;
	}
	// @RuleVersion(0)
	public adaptiveBlock(): AdaptiveBlockContext {
		let _localctx: AdaptiveBlockContext = new AdaptiveBlockContext(this._ctx, this.state);
		this.enterRule(_localctx, 18, dnaorganismParser.RULE_adaptiveBlock);
		let _la: number;
		try {
			this.enterOuterAlt(_localctx, 1);
			{
			this.state = 107;
			this.match(dnaorganismParser.ADAPTIVE_RES);
			this.state = 108;
			this.match(dnaorganismParser.LBRACE);
			this.state = 112;
			this._errHandler.sync(this);
			_la = this._input.LA(1);
			while (_la === dnaorganismParser.ID) {
				{
				{
				this.state = 109;
				this.attrPair();
				}
				}
				this.state = 114;
				this._errHandler.sync(this);
				_la = this._input.LA(1);
			}
			this.state = 115;
			this.match(dnaorganismParser.RBRACE);
			}
		}
		catch (re) {
			if (re instanceof RecognitionException) {
				_localctx.exception = re;
				this._errHandler.reportError(this, re);
				this._errHandler.recover(this, re);
			} else {
				throw re;
			}
		}
		finally {
			this.exitRule();
		}
		return _localctx;
	}
	// @RuleVersion(0)
	public agentsBlock(): AgentsBlockContext {
		let _localctx: AgentsBlockContext = new AgentsBlockContext(this._ctx, this.state);
		this.enterRule(_localctx, 20, dnaorganismParser.RULE_agentsBlock);
		let _la: number;
		try {
			this.enterOuterAlt(_localctx, 1);
			{
			this.state = 117;
			this.match(dnaorganismParser.AGENTS);
			this.state = 118;
			this.match(dnaorganismParser.LBRACE);
			this.state = 122;
			this._errHandler.sync(this);
			_la = this._input.LA(1);
			while (_la === dnaorganismParser.ID) {
				{
				{
				this.state = 119;
				this.agentAssign();
				}
				}
				this.state = 124;
				this._errHandler.sync(this);
				_la = this._input.LA(1);
			}
			this.state = 125;
			this.match(dnaorganismParser.RBRACE);
			}
		}
		catch (re) {
			if (re instanceof RecognitionException) {
				_localctx.exception = re;
				this._errHandler.reportError(this, re);
				this._errHandler.recover(this, re);
			} else {
				throw re;
			}
		}
		finally {
			this.exitRule();
		}
		return _localctx;
	}
	// @RuleVersion(0)
	public agentAssign(): AgentAssignContext {
		let _localctx: AgentAssignContext = new AgentAssignContext(this._ctx, this.state);
		this.enterRule(_localctx, 22, dnaorganismParser.RULE_agentAssign);
		try {
			this.enterOuterAlt(_localctx, 1);
			{
			this.state = 127;
			this.match(dnaorganismParser.ID);
			this.state = 128;
			this.match(dnaorganismParser.COLON);
			this.state = 129;
			this.match(dnaorganismParser.ID);
			this.state = 130;
			this.match(dnaorganismParser.SEMI);
			}
		}
		catch (re) {
			if (re instanceof RecognitionException) {
				_localctx.exception = re;
				this._errHandler.reportError(this, re);
				this._errHandler.recover(this, re);
			} else {
				throw re;
			}
		}
		finally {
			this.exitRule();
		}
		return _localctx;
	}
	// @RuleVersion(0)
	public attrPair(): AttrPairContext {
		let _localctx: AttrPairContext = new AttrPairContext(this._ctx, this.state);
		this.enterRule(_localctx, 24, dnaorganismParser.RULE_attrPair);
		let _la: number;
		try {
			this.enterOuterAlt(_localctx, 1);
			{
			this.state = 132;
			this.match(dnaorganismParser.ID);
			this.state = 133;
			this.match(dnaorganismParser.COLON);
			this.state = 134;
			_la = this._input.LA(1);
			if (!(_la === dnaorganismParser.STRING || _la === dnaorganismParser.NUMBER)) {
			this._errHandler.recoverInline(this);
			} else {
				if (this._input.LA(1) === Token.EOF) {
					this.matchedEOF = true;
				}

				this._errHandler.reportMatch(this);
				this.consume();
			}
			this.state = 135;
			this.match(dnaorganismParser.SEMI);
			}
		}
		catch (re) {
			if (re instanceof RecognitionException) {
				_localctx.exception = re;
				this._errHandler.reportError(this, re);
				this._errHandler.recover(this, re);
			} else {
				throw re;
			}
		}
		finally {
			this.exitRule();
		}
		return _localctx;
	}

	public static readonly _serializedATN: string =
		"\x03\uC91D\uCABA\u058D\uAFBA\u4F53\u0607\uEA8B\uC241\x03\x15\x8C\x04\x02" +
		"\t\x02\x04\x03\t\x03\x04\x04\t\x04\x04\x05\t\x05\x04\x06\t\x06\x04\x07" +
		"\t\x07\x04\b\t\b\x04\t\t\t\x04\n\t\n\x04\v\t\v\x04\f\t\f\x04\r\t\r\x04" +
		"\x0E\t\x0E\x03\x02\x07\x02\x1E\n\x02\f\x02\x0E\x02!\v\x02\x03\x02\x03" +
		"\x02\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03" +
		"\x04\x03\x04\x03\x04\x07\x040\n\x04\f\x04\x0E\x043\v\x04\x03\x04\x03\x04" +
		"\x03\x05\x03\x05\x03\x05\x07\x05:\n\x05\f\x05\x0E\x05=\v\x05\x03\x05\x03" +
		"\x05\x03\x06\x03\x06\x03\x06\x03\x06\x03\x06\x03\x06\x03\x07\x03\x07\x03" +
		"\x07\x03\x07\x07\x07K\n\x07\f\x07\x0E\x07N\v\x07\x03\b\x03\b\x03\b\x07" +
		"\bS\n\b\f\b\x0E\bV\v\b\x03\b\x03\b\x03\t\x03\t\x03\t\x07\t]\n\t\f\t\x0E" +
		"\t`\v\t\x03\t\x03\t\x03\n\x03\n\x03\n\x07\ng\n\n\f\n\x0E\nj\v\n\x03\n" +
		"\x03\n\x03\v\x03\v\x03\v\x07\vq\n\v\f\v\x0E\vt\v\v\x03\v\x03\v\x03\f\x03" +
		"\f\x03\f\x07\f{\n\f\f\f\x0E\f~\v\f\x03\f\x03\f\x03\r\x03\r\x03\r\x03\r" +
		"\x03\r\x03\x0E\x03\x0E\x03\x0E\x03\x0E\x03\x0E\x03\x0E\x02\x02\x02\x0F" +
		"\x02\x02\x04\x02\x06\x02\b\x02\n\x02\f\x02\x0E\x02\x10\x02\x12\x02\x14" +
		"\x02\x16\x02\x18\x02\x1A\x02\x02\x03\x03\x02\f\r\x02\x8A\x02\x1F\x03\x02" +
		"\x02\x02\x04$\x03\x02\x02\x02\x06,\x03\x02\x02\x02\b6\x03\x02\x02\x02" +
		"\n@\x03\x02\x02\x02\fL\x03\x02\x02\x02\x0EO\x03\x02\x02\x02\x10Y\x03\x02" +
		"\x02\x02\x12c\x03\x02\x02\x02\x14m\x03\x02\x02\x02\x16w\x03\x02\x02\x02" +
		"\x18\x81\x03\x02\x02\x02\x1A\x86\x03\x02\x02\x02\x1C\x1E\x05\x04\x03\x02" +
		"\x1D\x1C\x03\x02\x02\x02\x1E!\x03\x02\x02\x02\x1F\x1D\x03\x02\x02\x02" +
		"\x1F \x03\x02\x02\x02 \"\x03\x02\x02\x02!\x1F\x03\x02\x02\x02\"#\x07\x02" +
		"\x02\x03#\x03\x03\x02\x02\x02$%\x07\x03\x02\x02%&\x07\v\x02\x02&\'\x07" +
		"\x0E\x02\x02\'(\x05\x06\x04\x02()\x05\b\x05\x02)*\x05\x16\f\x02*+\x07" +
		"\x0F\x02\x02+\x05\x03\x02\x02\x02,-\x07\x05\x02\x02-1\x07\x0E\x02\x02" +
		".0\x05\x1A\x0E\x02/.\x03\x02\x02\x0203\x03\x02\x02\x021/\x03\x02\x02\x02" +
		"12\x03\x02\x02\x0224\x03\x02\x02\x0231\x03\x02\x02\x0245\x07\x0F\x02\x02" +
		"5\x07\x03\x02\x02\x0267\x07\x06\x02\x027;\x07\x0E\x02\x028:\x05\n\x06" +
		"\x0298\x03\x02\x02\x02:=\x03\x02\x02\x02;9\x03\x02\x02\x02;<\x03\x02\x02" +
		"\x02<>\x03\x02\x02\x02=;\x03\x02\x02\x02>?\x07\x0F\x02\x02?\t\x03\x02" +
		"\x02\x02@A\x07\x04\x02\x02AB\x07\v\x02\x02BC\x07\x0E\x02\x02CD\x05\f\x07" +
		"\x02DE\x07\x0F\x02\x02E\v\x03\x02\x02\x02FK\x05\x1A\x0E\x02GK\x05\x0E" +
		"\b\x02HK\x05\x12\n\x02IK\x05\x14\v\x02JF\x03\x02\x02\x02JG\x03\x02\x02" +
		"\x02JH\x03\x02\x02\x02JI\x03\x02\x02\x02KN\x03\x02\x02\x02LJ\x03\x02\x02" +
		"\x02LM\x03\x02\x02\x02M\r\x03\x02\x02\x02NL\x03\x02\x02\x02OP\x07\t\x02" +
		"\x02PT\x07\x0E\x02\x02QS\x05\x10\t\x02RQ\x03\x02\x02\x02SV\x03\x02\x02" +
		"\x02TR\x03\x02\x02\x02TU\x03\x02\x02\x02UW\x03\x02\x02\x02VT\x03\x02\x02" +
		"\x02WX\x07\x0F\x02\x02X\x0F\x03\x02\x02\x02YZ\x07\v\x02\x02Z^\x07\x0E" +
		"\x02\x02[]\x05\x1A\x0E\x02\\[\x03\x02\x02\x02]`\x03\x02\x02\x02^\\\x03" +
		"\x02\x02\x02^_\x03\x02\x02\x02_a\x03\x02\x02\x02`^\x03\x02\x02\x02ab\x07" +
		"\x0F\x02\x02b\x11\x03\x02\x02\x02cd\x07\b\x02\x02dh\x07\x0E\x02\x02eg" +
		"\x05\x1A\x0E\x02fe\x03\x02\x02\x02gj\x03\x02\x02\x02hf\x03\x02\x02\x02" +
		"hi\x03\x02\x02\x02ik\x03\x02\x02\x02jh\x03\x02\x02\x02kl\x07\x0F\x02\x02" +
		"l\x13\x03\x02\x02\x02mn\x07\n\x02\x02nr\x07\x0E\x02\x02oq\x05\x1A\x0E" +
		"\x02po\x03\x02\x02\x02qt\x03\x02\x02\x02rp\x03\x02\x02\x02rs\x03\x02\x02" +
		"\x02su\x03\x02\x02\x02tr\x03\x02\x02\x02uv\x07\x0F\x02\x02v\x15\x03\x02" +
		"\x02\x02wx\x07\x07\x02\x02x|\x07\x0E\x02\x02y{\x05\x18\r\x02zy\x03\x02" +
		"\x02\x02{~\x03\x02\x02\x02|z\x03\x02\x02\x02|}\x03\x02\x02\x02}\x7F\x03" +
		"\x02\x02\x02~|\x03\x02\x02\x02\x7F\x80\x07\x0F\x02\x02\x80\x17\x03\x02" +
		"\x02\x02\x81\x82\x07\v\x02\x02\x82\x83\x07\x13\x02\x02\x83\x84\x07\v\x02" +
		"\x02\x84\x85\x07\x12\x02\x02\x85\x19\x03\x02\x02\x02\x86\x87\x07\v\x02" +
		"\x02\x87\x88\x07\x13\x02\x02\x88\x89\t\x02\x02\x02\x89\x8A\x07\x12\x02" +
		"\x02\x8A\x1B\x03\x02\x02\x02\f\x1F1;JLT^hr|";
	public static __ATN: ATN;
	public static get _ATN(): ATN {
		if (!dnaorganismParser.__ATN) {
			dnaorganismParser.__ATN = new ATNDeserializer().deserialize(Utils.toCharArray(dnaorganismParser._serializedATN));
		}

		return dnaorganismParser.__ATN;
	}

}

export class ProgramContext extends ParserRuleContext {
	public EOF(): TerminalNode { return this.getToken(dnaorganismParser.EOF, 0); }
	public organismDef(): OrganismDefContext[];
	public organismDef(i: number): OrganismDefContext;
	public organismDef(i?: number): OrganismDefContext | OrganismDefContext[] {
		if (i === undefined) {
			return this.getRuleContexts(OrganismDefContext);
		} else {
			return this.getRuleContext(i, OrganismDefContext);
		}
	}
	constructor(parent: ParserRuleContext | undefined, invokingState: number) {
		super(parent, invokingState);
	}
	// @Override
	public get ruleIndex(): number { return dnaorganismParser.RULE_program; }
	// @Override
	public enterRule(listener: dnaorganismListener): void {
		if (listener.enterProgram) {
			listener.enterProgram(this);
		}
	}
	// @Override
	public exitRule(listener: dnaorganismListener): void {
		if (listener.exitProgram) {
			listener.exitProgram(this);
		}
	}
	// @Override
	public accept<Result>(visitor: dnaorganismVisitor<Result>): Result {
		if (visitor.visitProgram) {
			return visitor.visitProgram(this);
		} else {
			return visitor.visitChildren(this);
		}
	}
}


export class OrganismDefContext extends ParserRuleContext {
	public DNAORGANISM(): TerminalNode { return this.getToken(dnaorganismParser.DNAORGANISM, 0); }
	public ID(): TerminalNode { return this.getToken(dnaorganismParser.ID, 0); }
	public LBRACE(): TerminalNode { return this.getToken(dnaorganismParser.LBRACE, 0); }
	public dnaBlock(): DnaBlockContext {
		return this.getRuleContext(0, DnaBlockContext);
	}
	public genomeBlock(): GenomeBlockContext {
		return this.getRuleContext(0, GenomeBlockContext);
	}
	public agentsBlock(): AgentsBlockContext {
		return this.getRuleContext(0, AgentsBlockContext);
	}
	public RBRACE(): TerminalNode { return this.getToken(dnaorganismParser.RBRACE, 0); }
	constructor(parent: ParserRuleContext | undefined, invokingState: number) {
		super(parent, invokingState);
	}
	// @Override
	public get ruleIndex(): number { return dnaorganismParser.RULE_organismDef; }
	// @Override
	public enterRule(listener: dnaorganismListener): void {
		if (listener.enterOrganismDef) {
			listener.enterOrganismDef(this);
		}
	}
	// @Override
	public exitRule(listener: dnaorganismListener): void {
		if (listener.exitOrganismDef) {
			listener.exitOrganismDef(this);
		}
	}
	// @Override
	public accept<Result>(visitor: dnaorganismVisitor<Result>): Result {
		if (visitor.visitOrganismDef) {
			return visitor.visitOrganismDef(this);
		} else {
			return visitor.visitChildren(this);
		}
	}
}


export class DnaBlockContext extends ParserRuleContext {
	public DNA(): TerminalNode { return this.getToken(dnaorganismParser.DNA, 0); }
	public LBRACE(): TerminalNode { return this.getToken(dnaorganismParser.LBRACE, 0); }
	public RBRACE(): TerminalNode { return this.getToken(dnaorganismParser.RBRACE, 0); }
	public attrPair(): AttrPairContext[];
	public attrPair(i: number): AttrPairContext;
	public attrPair(i?: number): AttrPairContext | AttrPairContext[] {
		if (i === undefined) {
			return this.getRuleContexts(AttrPairContext);
		} else {
			return this.getRuleContext(i, AttrPairContext);
		}
	}
	constructor(parent: ParserRuleContext | undefined, invokingState: number) {
		super(parent, invokingState);
	}
	// @Override
	public get ruleIndex(): number { return dnaorganismParser.RULE_dnaBlock; }
	// @Override
	public enterRule(listener: dnaorganismListener): void {
		if (listener.enterDnaBlock) {
			listener.enterDnaBlock(this);
		}
	}
	// @Override
	public exitRule(listener: dnaorganismListener): void {
		if (listener.exitDnaBlock) {
			listener.exitDnaBlock(this);
		}
	}
	// @Override
	public accept<Result>(visitor: dnaorganismVisitor<Result>): Result {
		if (visitor.visitDnaBlock) {
			return visitor.visitDnaBlock(this);
		} else {
			return visitor.visitChildren(this);
		}
	}
}


export class GenomeBlockContext extends ParserRuleContext {
	public GENOME(): TerminalNode { return this.getToken(dnaorganismParser.GENOME, 0); }
	public LBRACE(): TerminalNode { return this.getToken(dnaorganismParser.LBRACE, 0); }
	public RBRACE(): TerminalNode { return this.getToken(dnaorganismParser.RBRACE, 0); }
	public geneDef(): GeneDefContext[];
	public geneDef(i: number): GeneDefContext;
	public geneDef(i?: number): GeneDefContext | GeneDefContext[] {
		if (i === undefined) {
			return this.getRuleContexts(GeneDefContext);
		} else {
			return this.getRuleContext(i, GeneDefContext);
		}
	}
	constructor(parent: ParserRuleContext | undefined, invokingState: number) {
		super(parent, invokingState);
	}
	// @Override
	public get ruleIndex(): number { return dnaorganismParser.RULE_genomeBlock; }
	// @Override
	public enterRule(listener: dnaorganismListener): void {
		if (listener.enterGenomeBlock) {
			listener.enterGenomeBlock(this);
		}
	}
	// @Override
	public exitRule(listener: dnaorganismListener): void {
		if (listener.exitGenomeBlock) {
			listener.exitGenomeBlock(this);
		}
	}
	// @Override
	public accept<Result>(visitor: dnaorganismVisitor<Result>): Result {
		if (visitor.visitGenomeBlock) {
			return visitor.visitGenomeBlock(this);
		} else {
			return visitor.visitChildren(this);
		}
	}
}


export class GeneDefContext extends ParserRuleContext {
	public DNAGENE(): TerminalNode { return this.getToken(dnaorganismParser.DNAGENE, 0); }
	public ID(): TerminalNode { return this.getToken(dnaorganismParser.ID, 0); }
	public LBRACE(): TerminalNode { return this.getToken(dnaorganismParser.LBRACE, 0); }
	public geneBody(): GeneBodyContext {
		return this.getRuleContext(0, GeneBodyContext);
	}
	public RBRACE(): TerminalNode { return this.getToken(dnaorganismParser.RBRACE, 0); }
	constructor(parent: ParserRuleContext | undefined, invokingState: number) {
		super(parent, invokingState);
	}
	// @Override
	public get ruleIndex(): number { return dnaorganismParser.RULE_geneDef; }
	// @Override
	public enterRule(listener: dnaorganismListener): void {
		if (listener.enterGeneDef) {
			listener.enterGeneDef(this);
		}
	}
	// @Override
	public exitRule(listener: dnaorganismListener): void {
		if (listener.exitGeneDef) {
			listener.exitGeneDef(this);
		}
	}
	// @Override
	public accept<Result>(visitor: dnaorganismVisitor<Result>): Result {
		if (visitor.visitGeneDef) {
			return visitor.visitGeneDef(this);
		} else {
			return visitor.visitChildren(this);
		}
	}
}


export class GeneBodyContext extends ParserRuleContext {
	public attrPair(): AttrPairContext[];
	public attrPair(i: number): AttrPairContext;
	public attrPair(i?: number): AttrPairContext | AttrPairContext[] {
		if (i === undefined) {
			return this.getRuleContexts(AttrPairContext);
		} else {
			return this.getRuleContext(i, AttrPairContext);
		}
	}
	public mutationsBlock(): MutationsBlockContext[];
	public mutationsBlock(i: number): MutationsBlockContext;
	public mutationsBlock(i?: number): MutationsBlockContext | MutationsBlockContext[] {
		if (i === undefined) {
			return this.getRuleContexts(MutationsBlockContext);
		} else {
			return this.getRuleContext(i, MutationsBlockContext);
		}
	}
	public immuneBlock(): ImmuneBlockContext[];
	public immuneBlock(i: number): ImmuneBlockContext;
	public immuneBlock(i?: number): ImmuneBlockContext | ImmuneBlockContext[] {
		if (i === undefined) {
			return this.getRuleContexts(ImmuneBlockContext);
		} else {
			return this.getRuleContext(i, ImmuneBlockContext);
		}
	}
	public adaptiveBlock(): AdaptiveBlockContext[];
	public adaptiveBlock(i: number): AdaptiveBlockContext;
	public adaptiveBlock(i?: number): AdaptiveBlockContext | AdaptiveBlockContext[] {
		if (i === undefined) {
			return this.getRuleContexts(AdaptiveBlockContext);
		} else {
			return this.getRuleContext(i, AdaptiveBlockContext);
		}
	}
	constructor(parent: ParserRuleContext | undefined, invokingState: number) {
		super(parent, invokingState);
	}
	// @Override
	public get ruleIndex(): number { return dnaorganismParser.RULE_geneBody; }
	// @Override
	public enterRule(listener: dnaorganismListener): void {
		if (listener.enterGeneBody) {
			listener.enterGeneBody(this);
		}
	}
	// @Override
	public exitRule(listener: dnaorganismListener): void {
		if (listener.exitGeneBody) {
			listener.exitGeneBody(this);
		}
	}
	// @Override
	public accept<Result>(visitor: dnaorganismVisitor<Result>): Result {
		if (visitor.visitGeneBody) {
			return visitor.visitGeneBody(this);
		} else {
			return visitor.visitChildren(this);
		}
	}
}


export class MutationsBlockContext extends ParserRuleContext {
	public MUTATIONS(): TerminalNode { return this.getToken(dnaorganismParser.MUTATIONS, 0); }
	public LBRACE(): TerminalNode { return this.getToken(dnaorganismParser.LBRACE, 0); }
	public RBRACE(): TerminalNode { return this.getToken(dnaorganismParser.RBRACE, 0); }
	public mutationDef(): MutationDefContext[];
	public mutationDef(i: number): MutationDefContext;
	public mutationDef(i?: number): MutationDefContext | MutationDefContext[] {
		if (i === undefined) {
			return this.getRuleContexts(MutationDefContext);
		} else {
			return this.getRuleContext(i, MutationDefContext);
		}
	}
	constructor(parent: ParserRuleContext | undefined, invokingState: number) {
		super(parent, invokingState);
	}
	// @Override
	public get ruleIndex(): number { return dnaorganismParser.RULE_mutationsBlock; }
	// @Override
	public enterRule(listener: dnaorganismListener): void {
		if (listener.enterMutationsBlock) {
			listener.enterMutationsBlock(this);
		}
	}
	// @Override
	public exitRule(listener: dnaorganismListener): void {
		if (listener.exitMutationsBlock) {
			listener.exitMutationsBlock(this);
		}
	}
	// @Override
	public accept<Result>(visitor: dnaorganismVisitor<Result>): Result {
		if (visitor.visitMutationsBlock) {
			return visitor.visitMutationsBlock(this);
		} else {
			return visitor.visitChildren(this);
		}
	}
}


export class MutationDefContext extends ParserRuleContext {
	public ID(): TerminalNode { return this.getToken(dnaorganismParser.ID, 0); }
	public LBRACE(): TerminalNode { return this.getToken(dnaorganismParser.LBRACE, 0); }
	public RBRACE(): TerminalNode { return this.getToken(dnaorganismParser.RBRACE, 0); }
	public attrPair(): AttrPairContext[];
	public attrPair(i: number): AttrPairContext;
	public attrPair(i?: number): AttrPairContext | AttrPairContext[] {
		if (i === undefined) {
			return this.getRuleContexts(AttrPairContext);
		} else {
			return this.getRuleContext(i, AttrPairContext);
		}
	}
	constructor(parent: ParserRuleContext | undefined, invokingState: number) {
		super(parent, invokingState);
	}
	// @Override
	public get ruleIndex(): number { return dnaorganismParser.RULE_mutationDef; }
	// @Override
	public enterRule(listener: dnaorganismListener): void {
		if (listener.enterMutationDef) {
			listener.enterMutationDef(this);
		}
	}
	// @Override
	public exitRule(listener: dnaorganismListener): void {
		if (listener.exitMutationDef) {
			listener.exitMutationDef(this);
		}
	}
	// @Override
	public accept<Result>(visitor: dnaorganismVisitor<Result>): Result {
		if (visitor.visitMutationDef) {
			return visitor.visitMutationDef(this);
		} else {
			return visitor.visitChildren(this);
		}
	}
}


export class ImmuneBlockContext extends ParserRuleContext {
	public IMMUNE_SYS(): TerminalNode { return this.getToken(dnaorganismParser.IMMUNE_SYS, 0); }
	public LBRACE(): TerminalNode { return this.getToken(dnaorganismParser.LBRACE, 0); }
	public RBRACE(): TerminalNode { return this.getToken(dnaorganismParser.RBRACE, 0); }
	public attrPair(): AttrPairContext[];
	public attrPair(i: number): AttrPairContext;
	public attrPair(i?: number): AttrPairContext | AttrPairContext[] {
		if (i === undefined) {
			return this.getRuleContexts(AttrPairContext);
		} else {
			return this.getRuleContext(i, AttrPairContext);
		}
	}
	constructor(parent: ParserRuleContext | undefined, invokingState: number) {
		super(parent, invokingState);
	}
	// @Override
	public get ruleIndex(): number { return dnaorganismParser.RULE_immuneBlock; }
	// @Override
	public enterRule(listener: dnaorganismListener): void {
		if (listener.enterImmuneBlock) {
			listener.enterImmuneBlock(this);
		}
	}
	// @Override
	public exitRule(listener: dnaorganismListener): void {
		if (listener.exitImmuneBlock) {
			listener.exitImmuneBlock(this);
		}
	}
	// @Override
	public accept<Result>(visitor: dnaorganismVisitor<Result>): Result {
		if (visitor.visitImmuneBlock) {
			return visitor.visitImmuneBlock(this);
		} else {
			return visitor.visitChildren(this);
		}
	}
}


export class AdaptiveBlockContext extends ParserRuleContext {
	public ADAPTIVE_RES(): TerminalNode { return this.getToken(dnaorganismParser.ADAPTIVE_RES, 0); }
	public LBRACE(): TerminalNode { return this.getToken(dnaorganismParser.LBRACE, 0); }
	public RBRACE(): TerminalNode { return this.getToken(dnaorganismParser.RBRACE, 0); }
	public attrPair(): AttrPairContext[];
	public attrPair(i: number): AttrPairContext;
	public attrPair(i?: number): AttrPairContext | AttrPairContext[] {
		if (i === undefined) {
			return this.getRuleContexts(AttrPairContext);
		} else {
			return this.getRuleContext(i, AttrPairContext);
		}
	}
	constructor(parent: ParserRuleContext | undefined, invokingState: number) {
		super(parent, invokingState);
	}
	// @Override
	public get ruleIndex(): number { return dnaorganismParser.RULE_adaptiveBlock; }
	// @Override
	public enterRule(listener: dnaorganismListener): void {
		if (listener.enterAdaptiveBlock) {
			listener.enterAdaptiveBlock(this);
		}
	}
	// @Override
	public exitRule(listener: dnaorganismListener): void {
		if (listener.exitAdaptiveBlock) {
			listener.exitAdaptiveBlock(this);
		}
	}
	// @Override
	public accept<Result>(visitor: dnaorganismVisitor<Result>): Result {
		if (visitor.visitAdaptiveBlock) {
			return visitor.visitAdaptiveBlock(this);
		} else {
			return visitor.visitChildren(this);
		}
	}
}


export class AgentsBlockContext extends ParserRuleContext {
	public AGENTS(): TerminalNode { return this.getToken(dnaorganismParser.AGENTS, 0); }
	public LBRACE(): TerminalNode { return this.getToken(dnaorganismParser.LBRACE, 0); }
	public RBRACE(): TerminalNode { return this.getToken(dnaorganismParser.RBRACE, 0); }
	public agentAssign(): AgentAssignContext[];
	public agentAssign(i: number): AgentAssignContext;
	public agentAssign(i?: number): AgentAssignContext | AgentAssignContext[] {
		if (i === undefined) {
			return this.getRuleContexts(AgentAssignContext);
		} else {
			return this.getRuleContext(i, AgentAssignContext);
		}
	}
	constructor(parent: ParserRuleContext | undefined, invokingState: number) {
		super(parent, invokingState);
	}
	// @Override
	public get ruleIndex(): number { return dnaorganismParser.RULE_agentsBlock; }
	// @Override
	public enterRule(listener: dnaorganismListener): void {
		if (listener.enterAgentsBlock) {
			listener.enterAgentsBlock(this);
		}
	}
	// @Override
	public exitRule(listener: dnaorganismListener): void {
		if (listener.exitAgentsBlock) {
			listener.exitAgentsBlock(this);
		}
	}
	// @Override
	public accept<Result>(visitor: dnaorganismVisitor<Result>): Result {
		if (visitor.visitAgentsBlock) {
			return visitor.visitAgentsBlock(this);
		} else {
			return visitor.visitChildren(this);
		}
	}
}


export class AgentAssignContext extends ParserRuleContext {
	public ID(): TerminalNode[];
	public ID(i: number): TerminalNode;
	public ID(i?: number): TerminalNode | TerminalNode[] {
		if (i === undefined) {
			return this.getTokens(dnaorganismParser.ID);
		} else {
			return this.getToken(dnaorganismParser.ID, i);
		}
	}
	public COLON(): TerminalNode { return this.getToken(dnaorganismParser.COLON, 0); }
	public SEMI(): TerminalNode { return this.getToken(dnaorganismParser.SEMI, 0); }
	constructor(parent: ParserRuleContext | undefined, invokingState: number) {
		super(parent, invokingState);
	}
	// @Override
	public get ruleIndex(): number { return dnaorganismParser.RULE_agentAssign; }
	// @Override
	public enterRule(listener: dnaorganismListener): void {
		if (listener.enterAgentAssign) {
			listener.enterAgentAssign(this);
		}
	}
	// @Override
	public exitRule(listener: dnaorganismListener): void {
		if (listener.exitAgentAssign) {
			listener.exitAgentAssign(this);
		}
	}
	// @Override
	public accept<Result>(visitor: dnaorganismVisitor<Result>): Result {
		if (visitor.visitAgentAssign) {
			return visitor.visitAgentAssign(this);
		} else {
			return visitor.visitChildren(this);
		}
	}
}


export class AttrPairContext extends ParserRuleContext {
	public ID(): TerminalNode { return this.getToken(dnaorganismParser.ID, 0); }
	public COLON(): TerminalNode { return this.getToken(dnaorganismParser.COLON, 0); }
	public SEMI(): TerminalNode { return this.getToken(dnaorganismParser.SEMI, 0); }
	public STRING(): TerminalNode | undefined { return this.tryGetToken(dnaorganismParser.STRING, 0); }
	public NUMBER(): TerminalNode | undefined { return this.tryGetToken(dnaorganismParser.NUMBER, 0); }
	constructor(parent: ParserRuleContext | undefined, invokingState: number) {
		super(parent, invokingState);
	}
	// @Override
	public get ruleIndex(): number { return dnaorganismParser.RULE_attrPair; }
	// @Override
	public enterRule(listener: dnaorganismListener): void {
		if (listener.enterAttrPair) {
			listener.enterAttrPair(this);
		}
	}
	// @Override
	public exitRule(listener: dnaorganismListener): void {
		if (listener.exitAttrPair) {
			listener.exitAttrPair(this);
		}
	}
	// @Override
	public accept<Result>(visitor: dnaorganismVisitor<Result>): Result {
		if (visitor.visitAttrPair) {
			return visitor.visitAttrPair(this);
		} else {
			return visitor.visitChildren(this);
		}
	}
}


