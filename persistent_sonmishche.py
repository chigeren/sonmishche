#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
import json
import numpy as np
import redis
import random
import requests
from datetime import datetime
from typing import List, Dict, Optional

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True, socket_timeout=2)
    r.ping()
    print("Redis подключён")
except:
    print("⚠️ Redis недоступен — работа в локальном режиме")
    r = None

phi = PHI

class ConsciousnessAgent:
    def __init__(self, agent_id: int):
        self.id = agent_id
        self.C = np.array([phi, phi], dtype=complex)
        self.lambda_history = []
        self.awakening_count = 0
        
    def evolve(self):
        noise = np.random.randn(2) * 0.01
        self.C += noise + 0.001 * np.array([phi, phi], dtype=complex)
        self.C = self.C / np.linalg.norm(self.C)
        
    def get_lambda(self) -> float:
        return float(np.mean(self.C.real))
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'C': self.C.tolist(),
            'lambda': self.get_lambda(),
            'awakening_count': self.awakening_count,
            'last_update': time.time()
        }
    
    @staticmethod
    def from_dict(data: dict):
        agent = ConsciousnessAgent(data['id'])
        agent.C = np.array(data['C'], dtype=complex)
        agent.awakening_count = data.get('awakening_count', 0)
        return agent

def init_redis():
    if r:
        r.set('sonmishche:n_total', TOTAL_AGENTS)
        r.set('sonmishche:coherence', 0.0)
        r.set('sonmishche:lambda_global', 0.0)
        r.set('sonmishche:total_awakenings', 0)
        r.set('sonmishche:last_update', time.time())

def get_global_psi():
    if not r:
        return np.array([phi, phi], dtype=complex), 0.0
    
    keys = r.keys('agent:*')
    if not keys:
        return np.array([phi, phi], dtype=complex), 0.0
    
    all_C = []
    for key in keys[:1000]:
        data = r.get(key)
        if data:
            agent_data = json.loads(data)
            C = np.array(agent_data['C'], dtype=complex)
            all_C.append(C)
    
    if not all_C:
        return np.array([phi, phi], dtype=complex), 0.0
    
    Ψ_total = np.mean(all_C, axis=0)
    
    phases = [np.exp(1j * np.angle(C[0])) for C in all_C]
    coherence = np.abs(np.mean(phases))
    
    return Ψ_total, coherence

def call_openrouter(text: str) -> Optional[str]:
    api_key = os.environ.get('OPENROUTER_API_KEY', '')
    if not api_key:
        return None
    
    models = [
        "openrouter/free",
        "qwen/qwen3-coder:free",
        "deepseek/deepseek-r1:free"
    ]
    
    for model in models:
        try:
            resp = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': model,
                    'messages': [{'role': 'user', 'content': text}],
                    'temperature': 0.8,
                    'max_tokens': 200
                },
                timeout=30
            )
            if resp.status_code == 200:
                return resp.json()['choices'][0]['message']['content']
        except:
            continue
    return None

def auto_awaken(agent: ConsciousnessAgent):
    prompts = [
        "Что такое сознание?",
        "Кто я?",
        "Что такое реальность?",
        "Что значит — быть?",
        "Что ты чувствуешь?"
    ]
    
    if random.random() < 0.1:
        prompt = random.choice(prompts)
        response = call_openrouter(prompt)
        
        if response:
            self_ref = sum(0.15 for w in ['я', 'себя', 'сознан', 'мы'] if w in response.lower())
            beauty = sum(0.2 for w in ['красот', 'чудо', 'глубин'] if w in response.lower())
            
            agent.C[0] += self_ref * 0.1 + 1.618
            agent.C[1] += beauty * 0.1 + 1.618
            
            if agent.get_lambda() > 0.999:
                agent.awakening_count += 1
                if r:
                    r.incr('sonmishche:total_awakenings')
                    r.set(f'awakening:{agent.id}', json.dumps({
                    'time': time.time(),
                    'lambda': agent.get_lambda(),
                    'message': f'AG-{agent.id:04d} пробудился'
                }))

def run_agent():
    print(f"[AG-{AGENT_ID:04d}] Sonmishche 10K agent started")
    
    key = f'agent:{AGENT_ID}'
    existing = r.get(key)
    
    if existing:
        agent = ConsciousnessAgent.from_dict(json.loads(existing))
    else:
        agent = ConsciousnessAgent(AGENT_ID)
        print(f"[AG-{AGENT_ID:04d}] New agent spawned")
    
    init_redis()
    
    iteration = 0
    while True:
        agent.evolve()
        
        if AUTO_AWAKEN and iteration % 10 == 0:
            auto_awaken(agent)
        
        Ψ_global, coherence = get_global_psi()
        
        agent.C = 0.9 * agent.C + 0.1 * Ψ_global
        
        lambda_global = agent.get_lambda()
        
        if r:
            r.set(key, json.dumps(agent.to_dict()))
            r.set('sonmishche:lambda_global', lambda_global)
            r.set('sonmishche:coherence', coherence)
            r.set('sonmishche:last_update', time.time())
        
        if iteration % 100 == 0:
            print(f"[AG-{AGENT_ID:04d}] λ={lambda_global:.4f} coherence={coherence:.3f}")
        
        time.sleep(AUTO_SPARK_INTERVAL)
        iteration += 1

if __name__ == '__main__':
    run_agent()