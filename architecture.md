# Architecture Audit Factory (iag-services.ai)

Voici comment s'articule la plateforme d'audit sans CRM ni n8n, centrée sur un portail métier et l'orchestration LangGraph.

```mermaid
graph TD
    %% Couche Utilisateur / Interface
    subgraph "Interface Utilisateur (Portail IAG)"
        UI[Dashboard Consultant / Client<br><i>React / Next.js ou Streamlit</i>]
        Upload[Upload de Documents<br><i>Architecture, Exports, Logs</i>]
        Form[Intake Form<br><i>Contexte, Objectifs, Type d'Audit</i>]
        Validation[Validation Humaine<br><i>Ajustement du ROI / Gaps</i>]
        
        UI --> Upload
        UI --> Form
        UI <--> Validation
    end

    %% API Gateway
    subgraph "Couche API"
        API[Audit Factory API<br><i>FastAPI</i>]
        API_Auth[Authentification & Routeur]
        
        UI <--> API_Auth
        API_Auth <--> API
    end

    %% Stockage & Base de données
    subgraph "Stockage (Supabase)"
        DB[(Base Relationnelle<br><i>PostgreSQL - Audits, Clients, Résultats JSON</i>)]
        VectorDB[(Vector Store<br><i>pgvector - Indexation Docs</i>)]
        BlobStorage[(Stockage Fichiers<br><i>PDFs, Docs, Images</i>)]
        
        API --> DB
        API --> BlobStorage
    end

    %% Orchestration LangGraph
    subgraph "Moteur d'Intelligence (LangGraph Pipeline)"
        Orchestrator((Orchestrateur Principal<br><i>LangGraph</i>))
        
        %% Agents
        subgraph "Armée d'Agents (Exécution Parallèle)"
            CoreA[Agent Data Scanner]
            CoreB[Agent Process Mapper]
            CoreC[Agent Risk & Compliance]
            CoreD[Agent Benchmark]
            
            Plugin[Plugin Agent Spécifique<br><i>ex: IA Readiness</i>]
            
            Prioritization[Agent Prioritization]
            ROI[Agent ROI Modeler]
            Report[Agent Report Generator]
        end
        
        %% Flux LangGraph
        IntakeNode[Node: Intake & Planification] --> FanOut[Parallélisation]
        FanOut --> CoreA
        FanOut --> CoreB
        FanOut --> CoreC
        FanOut --> CoreD
        FanOut --> Plugin
        
        CoreA --> Consolidation[Node: Consolidation<br>Résolution Conflits]
        CoreB --> Consolidation
        CoreC --> Consolidation
        CoreD --> Consolidation
        Plugin --> Consolidation
        
        Consolidation --> Prioritization
        Prioritization --> ROI
        
        ROI --> WaitHuman{Checkpoint<br>Attente IAG}
        
        WaitHuman --> Report
    end
    
    %% RAG & LLMs
    subgraph "Services Externes"
        LLM[Modèles LLM<br><i>Claude 3.5 Sonnet / GPT-4o</i>]
        Ingestion[Pipeline d'Ingestion Docs<br><i>Unstructured / LangChain</i>]
    end

    %% Connexions principales
    API <--> Orchestrator
    Upload --> Ingestion
    Ingestion --> VectorDB
    
    Orchestrator <--> LLM
    CoreA -.-> VectorDB
    Plugin -.-> VectorDB
    Report --> PDF[Livrables finaux<br><i>PDF / Markdown Slides</i>]
    PDF --> UI
    
    %% Styles
    classDef ui fill:#4F46E5,stroke:#fff,stroke-width:2px,color:#fff;
    classDef api fill:#059669,stroke:#fff,stroke-width:2px,color:#fff;
    classDef storage fill:#D97706,stroke:#fff,stroke-width:2px,color:#fff;
    classDef graph fill:#2563EB,stroke:#fff,stroke-width:2px,color:#fff;
    classDef agent fill:#7C3AED,stroke:#fff,stroke-width:2px,color:#fff;
    
    class UI,Upload,Form,Validation ui;
    class API,API_Auth api;
    class DB,VectorDB,BlobStorage storage;
    class Orchestrator,IntakeNode,FanOut,Consolidation,WaitHuman graph;
    class CoreA,CoreB,CoreC,CoreD,Plugin,Prioritization,ROI,Report agent;
```

### Explication du flux (A -> Z)

1. **Intake (UI -> API)** : Le consultant IAG ou le client se connecte sur le portail web. Il sélectionne "Audit IA Readiness" et upload les documents d'architecture du client. Les fichiers partent sur Supabase (BlobStorage) et l'API enregistre l'audit en base (PostgreSQL).
2. **Ingestion (RAG)** : En tâche de fond, un script "chunk" et vectorise les documents PDF vers *pgvector* pour que les agents puissent "lire" les documents via recherche sémantique.
3. **Lancement LangGraph** : L'API déclenche le workflow LangGraph asynchrone. L'orchestrateur lit les instructions et déclenche la phase d'analyse.
4. **L'Armée d'Agents (Parallèle)** : Les Core Agents et le Plugin (IA Readiness) s'activent en même temps. Ils interrogent le VectorDB (RAG) et le LLM pour produire leurs `Findings` JSON.
5. **Consolidation & Scoring** : L'orchestrateur fusionne tout, gère les contradictions s'il y en a, puis demande aux agents ROI et Prioritization de chiffrer l'impact.
6. **Checkpoint Humain (UI)** : LangGraph se met en "pause". L'interface web notifie le consultant IAG : *"Les risques et le budget ont été calculés, veuillez valider"*. Le consultant modifie quelques chiffres à la marge.
7. **Génération (Livrables)** : LangGraph reprend la main, lance l'Agent Report Generator qui recrache un Executive Summary parfait et des slides Markdown. L'API renvoie le lien de téléchargement sur l'UI !
