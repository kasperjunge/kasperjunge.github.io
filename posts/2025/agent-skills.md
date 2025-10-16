---
blogpost: true
date: Oct 16, 2025
author: Kasper Junge
language: Danish
---

# Agent Skills
 
Anthropic har netop launch’et konceptet “Skills” på tværs af Claude Apps, Claude Code og Claude API.

## Hvad er en Agent Skill?

En skill består af en mappe med en SKILL.md-fil og et vilkårligt antal filer.

En skill har tre niveauer af detalje:

1. Navn og beskrivelse
2. Brødteksten i SKILL.md
3. Eventuelle filer i skill-mappen

Navn og beskrivelse bruges af agenten til at vurdere, om den skal bruge skill’en eller ej - præcis ligesom MCP.

## Hvordan fungerer Skills?

Brødteksten i SKILL.md fungerer som en form for manual med en indholdsfortegnelse.
Filerne i skill-mappen kan være markdown-filer med brugbar information til den pågældende skill eller kode, som kan eksekveres.

Anthropic kalder det for “progressive disclosure” - at agenten ikke behøver al information på én gang, men kan dykke ned i den information og funktionalitet, der er knyttet til en skill, gradvist efter behov.

Kort sagt: Skills gør det muligt at bygge composable viden og evner, som agenter kan dele.

## Hvorfor er det vigtigt?

For dem, der ikke kan se potentialet i prompt- og context engineering, kan primitives som commands og subagents, som Anthropic har introduceret i Claude Code, virke basale, fjollede og antropomorfiserende.

Men det er tydeligt, at Anthropic er længst fremme, når det gælder primitives for agenter, hvilket jeg tror i høj grad skyldes det fantastiske udvikler community de har fået op at køre omkring Claude Code.

I begyndelsen handlede Claude Code om at bygge AI-kodeagenter, men udviklerne fandt hurtigt ud af, at Claude Code og den dertilhørende SDK fungerede supergodt som et generelt agentudviklingsværktøj - ikke kun til kode.

Det er også årsagen til, at Anthropic netop har omdøbt Claude Code SDK til det mere generelle Claude Agent SDK.

Anthropic står bag flere nyskabelser som MCP, subagents og commands - alle værktøjer, der løfter context engineering til næste niveau.

De gør det lettere at:

- delegere indhentning og generering af kontekst
- standardisere udstillingen af funktionalitet
- genbruge prompts, så man investerer i sine prompts i stedet for at smide dem væk.

## Bliver det stort?

Jeg har stor tillid til, at Anthropics ræsonnement bag at introducere Skills kommer af et hav af iterationer, hvor behovet for netop dette koncept er blevet klart for udviklerne hos Anthropic.

Skills gør det muligt at komponere en agents evner med specifikke instruktioner, ressourcer og scripts, som agenten kan afvikle.


Anthropic nævner også et muligt marketplace for skills - noget, der potentielt kan udvikle sig til et slags pakkeindex for AI-agenter, på samme måde som PyPI er for Python.

Der er efter min mening ingen tvivl om at Anthropic er ledende, når det gælder opbygningen af et åbent økosystem for agent context engineering.

Jeg tror, Anthropic har ramt den lige i røven her. 

Igen.

Læs mere om Agent Skills her:

https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

