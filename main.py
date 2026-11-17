"""
================================================================================
                    COSMIC VANGUARD: VOID RECURSION
================================================================================
A retro-arcade space shooter built in Python demonstrating:
  1. BASIC LOOPS:
     - Main game loop (while running)
     - Entity update & rendering loops (for item in list)
     - Collision detection loops (nested for loops)
     - Parallax starfield loops (for star in stars)
     - List filtering loops & comprehensions
  2. RECURSION:
     - Recursive Squadron Formation Generator: generates branching alien fleets
     - Recursive Chain Reaction Explosions: cascading bomb blast damage
     - Recursive Combo Score Calculator: mathematical recurrence relation
     - Recursive Fractal Nebula Generator: spatial midpoint/radial subdivision
     - Recursive Alien Cipher Decoder: recursive string manipulation
  3. BASIC SYNTAX & CONCEPTS:
     - Functions with type annotations and docstrings
     - Classes, objects, inheritance, and encapsulation
     - Conditionals (if, elif, else) and boolean logic
     - Data structures (lists, tuples, dictionaries, sets)
     - Arithmetic, assignment, and string formatting (f-strings)
     - Exception handling (try / except)
================================================================================
"""

import sys
import math
import random
import io
import wave
import struct
import pygame

# ==============================================================================
# SECTION 1: CONSTANTS & CONFIGURATION (Basic Syntax: Variables & Types)
# ==============================================================================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
FPS = 60

# RGB Color Tuples (Basic Syntax: Tuples & Numbers)
COLOR_BLACK       = (10, 10, 20)
COLOR_WHITE       = (255, 255, 255)
COLOR_CYAN        = (0, 255, 255)
COLOR_NEON_GREEN  = (57, 255, 20)
COLOR_HOT_PINK    = (255, 20, 147)
COLOR_YELLOW      = (255, 230, 0)
COLOR_RED         = (255, 50, 50)
COLOR_PURPLE      = (180, 50, 255)
COLOR_ORANGE      = (255, 140, 0)
COLOR_DARK_BLUE   = (15, 20, 45)
COLOR_HUD_BG      = (20, 25, 40, 200)

# ==============================================================================
# SECTION 2: PROCEDURAL AUDIO SYNTHESIZER (Basic Syntax: IO, Math, Struct)
# ==============================================================================
# Synthesizes retro arcade sound effects in memory using standard library math
# and wave modules. Gracefully handles systems without audio hardware.
# ==============================================================================

class SoundManager:
    """Manages audio generation and playback with graceful fallback."""
    def __init__(self):
        self.enabled = False
        self.sounds = {}
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.enabled = True
            self._generate_all_sounds()
        except Exception as error:
            print(f"[SoundManager] Audio initialization skipped: {error}")

    def _create_wav_sound(self, sample_generator, duration_sec: float, volume: float = 0.5):
        """Helper function using a basic loop to generate audio samples."""
        if not self.enabled:
            return None
        framerate = 44100
        total_samples = int(framerate * duration_sec)
        samples = []
        
        # BASIC LOOP: Generating audio sample amplitudes over time
        for i in range(total_samples):
            t = i / framerate
            amp = sample_generator(t, duration_sec)
            clamped = max(-1.0, min(1.0, amp))
            samples.append(int(clamped * 32767 * volume))
            
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(framerate)
            wf.writeframes(struct.pack(f'<{len(samples)}h', *samples))
        buffer.seek(0)
        return pygame.mixer.Sound(buffer)

    def _generate_all_sounds(self):
        """Generates procedural sound effects."""
        # 1. Laser Zap: Frequency drops rapidly from 900Hz to 250Hz
        self.sounds["laser"] = self._create_wav_sound(
            lambda t, d: math.sin(2 * math.pi * (900 - 650 * (t / d)) * t) * (1 - t / d),
            duration_sec=0.15, volume=0.3
        )
        # 2. Enemy Explosion: White noise mixed with low decaying frequency
        self.sounds["explosion"] = self._create_wav_sound(
            lambda t, d: (random.uniform(-1, 1) * 0.7 + math.sin(2 * math.pi * 120 * t) * 0.3) * (1 - t / d)**2,
            duration_sec=0.35, volume=0.45
        )
        # 3. EMP Shockwave: Low resonant sweep with wobble
        self.sounds["emp"] = self._create_wav_sound(
            lambda t, d: math.sin(2 * math.pi * (180 - 120 * (t / d) + 20 * math.sin(30 * t)) * t) * (1 - t / d),
            duration_sec=0.6, volume=0.6
        )
        # 4. Power-Up: Ascending arpeggio
        self.sounds["powerup"] = self._create_wav_sound(
            lambda t, d: math.sin(2 * math.pi * (400 + 600 * (t / d)) * t) * (1 - (t / d)**2),
            duration_sec=0.25, volume=0.4
        )
        # 5. Player Damage: Jarring buzz
        self.sounds["hit"] = self._create_wav_sound(
            lambda t, d: (1.0 if math.sin(2 * math.pi * 150 * t) > 0 else -1.0) * (1 - t / d) * 0.5,
            duration_sec=0.2, volume=0.35
        )

    def play(self, sound_name: str):
        """Plays a generated sound effect if audio is active."""
        if self.enabled and sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].play()
            except Exception:
                pass


# ==============================================================================
# SECTION 3: RECURSION SHOWCASE (The Core Educational Recursive Functions)
# ==============================================================================

def generate_formation_recursive(cx: float, cy: float, depth: int, 
                                 spread_x: float, spread_y: float, 
                                 wave_number: int) -> list:
    """
    RECURSION CONCEPT #1: Squadron Formation Generator
    --------------------------------------------------
    Generates a hierarchical, symmetrical alien attack fleet using recursion.
    
    - Base Case:
        When depth == 0, we reach the vanguard rank. Returns a single scout drone.
    - Recursive Step:
        Places a commander / cruiser ship at (cx, cy).
        Then recursively invokes itself to construct the Left Wing and Right Wing!
        Left Wing  = generate_formation_recursive(cx - spread_x, cy + spread_y, depth - 1, ...)
        Right Wing = generate_formation_recursive(cx + spread_x, cy + spread_y, depth - 1, ...)
        Combines [commander] + left_wing + right_wing.
    """
    # BASE CASE
    if depth <= 0:
        enemy_type = "scout"
        return [Enemy(cx, cy, enemy_type, wave_number)]

    # RECURSIVE STEP
    # Choose rank based on depth
    if depth >= 2:
        current_type = "dreadnought" if depth == 3 else "cruiser"
    else:
        current_type = "cruiser"
        
    current_ship = Enemy(cx, cy, current_type, wave_number)
    
    # Recursive calls for left and right wings with adjusted spacing
    left_wing = generate_formation_recursive(
        cx - spread_x, 
        cy + spread_y, 
        depth - 1, 
        spread_x * 0.75, 
        spread_y * 0.85, 
        wave_number
    )
    
    right_wing = generate_formation_recursive(
        cx + spread_x, 
        cy + spread_y, 
        depth - 1, 
        spread_x * 0.75, 
        spread_y * 0.85, 
        wave_number
    )
    
    # Combine the current ship with all recursive children
    return [current_ship] + left_wing + right_wing


def trigger_chain_reaction_recursive(origin_x: float, origin_y: float, 
                                    radius: float, depth: int, 
                                    enemies_list: list, 
                                    particles_list: list, 
                                    sound_mgr: SoundManager,
                                    decay_factor: float = 0.8) -> int:
    """
    RECURSION CONCEPT #2: Explosive Chain Reactions
    -----------------------------------------------
    When a critical shockwave or EMP detonates, it damages nearby enemies.
    If that explosion destroys adjacent ships, those ships ALSO explode,
    recursively propagating shockwaves across the fleet!
    
    - Base Case:
        1. depth <= 0: maximum blast propagation reached.
        2. radius < 15: blast energy dissipated.
        3. No alive enemies in proximity.
    - Recursive Step:
        For each newly detonated enemy, call trigger_chain_reaction_recursive
        with decaying radius and decremented depth.
    - Returns:
        Total number of ships eliminated throughout the recursive cascade.
    """
    # BASE CASE: Stop if chain reaction has expended maximum recursion depth
    if depth <= 0 or radius < 15:
        return 0

    chain_count = 0
    newly_destroyed = []

    # BASIC LOOP: Check proximity of living enemies to the blast epicenter
    for enemy in enemies_list:
        if enemy.alive:
            dist = math.hypot(enemy.x - origin_x, enemy.y - origin_y)
            if dist <= radius:
                # Calculate damage scaled by proximity
                damage = int(100 * (1 - dist / radius)) + 40
                killed = enemy.take_damage(damage)
                
                # Visual shockwave particles
                for _ in range(8):
                    particles_list.append(Particle(enemy.x, enemy.y, COLOR_CYAN, speed_scale=2.5))
                    
                if killed:
                    newly_destroyed.append(enemy)
                    chain_count += 1

    # RECURSIVE STEP: Each newly destroyed enemy detonates its own child explosion
    for destroyed_enemy in newly_destroyed:
        # Spawn massive explosive burst at child epicenter
        for _ in range(16):
            particles_list.append(Particle(destroyed_enemy.x, destroyed_enemy.y, COLOR_PURPLE, speed_scale=3.5))
            
        sound_mgr.play("explosion")
        
        # Recursive call: cascade to next depth level
        chain_count += trigger_chain_reaction_recursive(
            origin_x=destroyed_enemy.x,
            origin_y=destroyed_enemy.y,
            radius=radius * decay_factor,
            depth=depth - 1,
            enemies_list=enemies_list,
            particles_list=particles_list,
            sound_mgr=sound_mgr,
            decay_factor=decay_factor
        )

    return chain_count


def calc_combo_score_recursive(streak: int, base_points: int = 100) -> int:
    """
    RECURSION CONCEPT #3: Mathematical Combo Score Calculation
    ----------------------------------------------------------
    Calculates dynamic score rewards using recurrence relation:
      Score(0) = 0
      Score(1) = base_points
      Score(n) = n * base_points + int(1.15 * Score(n - 1))
      
    - Base Case:
        streak <= 0 returns 0
        streak == 1 returns base_points
    - Recursive Step:
        Score(n) compounds rewards for consecutive hits without missing.
    """
    # BASE CASES
    if streak <= 0:
        return 0
    if streak == 1:
        return base_points
        
    # RECURSIVE STEP
    return int((streak * base_points) + 1.15 * calc_combo_score_recursive(streak - 1, base_points))


def generate_fractal_nebula_recursive(cx: float, cy: float, radius: float, 
                                      depth: int, nebula_particles: list):
    """
    RECURSION CONCEPT #4: Fractal Nebula Generator
    ----------------------------------------------
    Generates a space nebula cloud through recursive radial subdivision.
    
    - Base Case:
        depth == 0 or radius < 10
    - Recursive Step:
        Appends a glowing gas node at (cx, cy), then branches in 3 sub-directions.
    """
    # BASE CASE
    if depth <= 0 or radius < 12:
        return

    # Add gas particle at current center
    color_choice = random.choice([COLOR_PURPLE, COLOR_HOT_PINK, COLOR_CYAN, COLOR_DARK_BLUE])
    nebula_particles.append({
        "x": cx + random.uniform(-radius * 0.3, radius * 0.3),
        "y": cy + random.uniform(-radius * 0.3, radius * 0.3),
        "radius": radius,
        "color": color_choice,
        "alpha": random.randint(30, 80)
    })

    # RECURSIVE STEP: Branch into 3 child nebula pockets
    for angle_deg in [30, 150, 270]:
        rad = math.radians(angle_deg + random.uniform(-20, 20))
        sub_x = cx + math.cos(rad) * (radius * 0.8)
        sub_y = cy + math.sin(rad) * (radius * 0.8)
        generate_fractal_nebula_recursive(sub_x, sub_y, radius * 0.6, depth - 1, nebula_particles)


def decode_alien_cipher_recursive(cipher_text: str) -> str:
    """
    RECURSION CONCEPT #5: Recursive String Reversal & Cipher Decoder
    ---------------------------------------------------------------
    Demonstrates structural recursion on strings.
    - Base Case:
        len(cipher_text) <= 1: a single character is already reversed.
    - Recursive Step:
        Take the last character + recursive reverse of the rest.
    """
    # BASE CASE
    if len(cipher_text) <= 1:
        return cipher_text
    # RECURSIVE STEP
    return cipher_text[-1] + decode_alien_cipher_recursive(cipher_text[:-1])


# ==============================================================================
# SECTION 4: GAME ENTITY CLASSES (Basic Syntax: OOP, Classes, Methods)
# ==============================================================================

class Star:
    """Represents a background star in the multi-layer parallax starfield."""
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.reset(random_y=True)

    def reset(self, random_y: bool = False):
        self.x = random.uniform(0, self.width)
        self.y = random.uniform(0, self.height) if random_y else 0
        self.layer = random.choice([1, 2, 3])  # 1 = distant (slow), 3 = close (fast)
        self.speed = self.layer * 1.2
        self.radius = self.layer
        self.brightness = 75 + self.layer * 60

    def update(self):
        self.y += self.speed
        if self.y > self.height:
            self.reset(random_y=False)

    def draw(self, surface: pygame.Surface):
        color = (self.brightness, self.brightness, min(255, self.brightness + 30))
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)


class Particle:
    """Explosion spark and engine exhaust particle."""
    def __init__(self, x: float, y: float, color: tuple, speed_scale: float = 1.0, is_exhaust: bool = False):
        self.x = x
        self.y = y
        self.color = color
        angle = random.uniform(0, math.pi * 2) if not is_exhaust else random.uniform(math.pi * 0.35, math.pi * 0.65)
        speed = random.uniform(1.0, 4.5) * speed_scale
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.randint(15, 35) if not is_exhaust else random.randint(6, 12)
        self.max_life = self.life
        self.radius = random.uniform(2.0, 4.0) if not is_exhaust else random.uniform(1.5, 3.0)

    def update(self) -> bool:
        """Updates particle physics. Returns False if dead."""
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.94
        self.vy *= 0.94
        self.life -= 1
        return self.life > 0

    def draw(self, surface: pygame.Surface):
        if self.life <= 0:
            return
        alpha_ratio = self.life / self.max_life
        current_radius = max(1, int(self.radius * alpha_ratio))
        # Draw with glowing circle
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), current_radius)


class FloatingText:
    """Floating combat text for scores and combo announcements."""
    def __init__(self, x: float, y: float, text: str, color: tuple, font: pygame.font.Font):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = font
        self.life = 45
        self.max_life = 45

    def update(self) -> bool:
        self.y -= 1.2
        self.life -= 1
        return self.life > 0

    def draw(self, surface: pygame.Surface):
        if self.life <= 0:
            return
        text_surf = self.font.render(self.text, True, self.color)
        surface.blit(text_surf, (int(self.x - text_surf.get_width() / 2), int(self.y)))


class Bullet:
    """Laser projectile for player and enemies."""
    def __init__(self, x: float, y: float, vy: float, is_player: bool = True, color: tuple = COLOR_CYAN):
        self.x = x
        self.y = y
        self.vy = vy
        self.is_player = is_player
        self.color = color
        self.width = 4
        self.height = 14
        self.alive = True

    def update(self):
        self.y += self.vy
        if self.y < -30 or self.y > SCREEN_HEIGHT + 30:
            self.alive = False

    def draw(self, surface: pygame.Surface):
        # Draw glowing laser capsule
        rect = pygame.Rect(int(self.x - self.width / 2), int(self.y - self.height / 2), self.width, self.height)
        pygame.draw.rect(surface, self.color, rect, border_radius=2)
        # Inner white core
        core_rect = pygame.Rect(int(self.x - 1), int(self.y - self.height / 2 + 2), 2, self.height - 4)
        pygame.draw.rect(surface, COLOR_WHITE, core_rect)


class PowerUp:
    """Collectible energy capsule dropped by high-rank enemies."""
    def __init__(self, x: float, y: float, p_type: str = "shield"):
        self.x = x
        self.y = y
        self.p_type = p_type  # "shield", "rapid", "bomb"
        self.vy = 2.0
        self.alive = True
        self.angle = 0.0

    def update(self):
        self.y += self.vy
        self.angle += 0.05
        if self.y > SCREEN_HEIGHT + 30:
            self.alive = False

    def draw(self, surface: pygame.Surface):
        color = COLOR_NEON_GREEN if self.p_type == "shield" else (COLOR_YELLOW if self.p_type == "rapid" else COLOR_PURPLE)
        # Pulsing diamond icon
        points = [
            (self.x, self.y - 10),
            (self.x + 10, self.y),
            (self.x, self.y + 10),
            (self.x - 10, self.y)
        ]
        pygame.draw.polygon(surface, color, points, width=2)
        pygame.draw.circle(surface, COLOR_WHITE, (int(self.x), int(self.y)), 3)


class Player:
    """Player Starfighter with responsive physics, weapons, and EMP."""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.speed = 6.5
        self.width = 38
        self.height = 42
        self.max_health = 100
        self.health = self.max_health
        self.lives = 3
        self.invulnerable_timer = 0
        self.fire_cooldown = 0
        self.rapid_fire_timer = 0
        self.emp_charges = 1
        self.max_emp_charges = 3
        self.emp_charge_progress = 0  # 0 to 100%

    def handle_input(self, keys: pygame.key.ScancodeWrapper, bullets: list, sound_mgr: SoundManager, particles: list):
        """Processes continuous keyboard inputs."""
        # Movement: Arrow keys or WASD
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed

        # Normalize diagonal movement speed
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        self.x += dx
        self.y += dy

        # Keep player ship clamped within window boundaries
        self.x = max(self.width / 2 + 10, min(SCREEN_WIDTH - self.width / 2 - 10, self.x))
        self.y = max(self.height / 2 + 50, min(SCREEN_HEIGHT - self.height / 2 - 15, self.y))

        # Thruster exhaust particles
        if random.random() < 0.8:
            particles.append(Particle(self.x - 7, self.y + 18, COLOR_CYAN, speed_scale=0.8, is_exhaust=True))
            particles.append(Particle(self.x + 7, self.y + 18, COLOR_CYAN, speed_scale=0.8, is_exhaust=True))

        # Primary Weapons: Spacebar
        cooldown_limit = 7 if self.rapid_fire_timer > 0 else 14
        if keys[pygame.K_SPACE]:
            if self.fire_cooldown <= 0:
                self.shoot(bullets, sound_mgr)
                self.fire_cooldown = cooldown_limit

    def shoot(self, bullets: list, sound_mgr: SoundManager):
        """Spawns dual or triple laser cannons."""
        sound_mgr.play("laser")
        if self.rapid_fire_timer > 0:
            # Triple cannon upgrade
            bullets.append(Bullet(self.x, self.y - 18, -12, is_player=True, color=COLOR_YELLOW))
            bullets.append(Bullet(self.x - 14, self.y - 10, -11, is_player=True, color=COLOR_YELLOW))
            bullets.append(Bullet(self.x + 14, self.y - 10, -11, is_player=True, color=COLOR_YELLOW))
        else:
            # Dual standard lasers
            bullets.append(Bullet(self.x - 12, self.y - 12, -10, is_player=True, color=COLOR_CYAN))
            bullets.append(Bullet(self.x + 12, self.y - 12, -10, is_player=True, color=COLOR_CYAN))

    def update(self):
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
        if self.rapid_fire_timer > 0:
            self.rapid_fire_timer -= 1

    def take_damage(self, amount: int, sound_mgr: SoundManager) -> bool:
        """Damages player unless invulnerable. Returns True if destroyed."""
        if self.invulnerable_timer > 0:
            return False
            
        self.health -= amount
        sound_mgr.play("hit")
        self.invulnerable_timer = 45  # Grace period immunity
        
        if self.health <= 0:
            self.lives -= 1
            if self.lives > 0:
                self.health = self.max_health
                self.invulnerable_timer = 90
            return True
        return False

    def draw(self, surface: pygame.Surface):
        # Flicker when invulnerable
        if self.invulnerable_timer > 0 and (self.invulnerable_timer // 4) % 2 == 0:
            return

        # Vector Fighter Polygon
        points = [
            (self.x, self.y - 20),           # Nose
            (self.x + 18, self.y + 15),       # Right wing tip
            (self.x + 10, self.y + 12),       # Right inner
            (self.x + 8, self.y + 18),        # Right engine
            (self.x, self.y + 14),            # Center thruster
            (self.x - 8, self.y + 18),        # Left engine
            (self.x - 10, self.y + 12),       # Left inner
            (self.x - 18, self.y + 15)        # Left wing tip
        ]
        
        # Hull outline & fill
        pygame.draw.polygon(surface, (25, 45, 80), points)
        pygame.draw.polygon(surface, COLOR_CYAN, points, width=2)
        
        # Cockpit canopy
        cockpit_points = [
            (self.x, self.y - 10),
            (self.x + 4, self.y + 2),
            (self.x, self.y + 5),
            (self.x - 4, self.y + 2)
        ]
        pygame.draw.polygon(surface, COLOR_HOT_PINK, cockpit_points)


class Enemy:
    """Alien warship with distinct combat behaviors and stats."""
    def __init__(self, x: float, y: float, enemy_type: str, wave_number: int):
        self.x = x
        self.y = y
        self.original_x = x
        self.enemy_type = enemy_type
        self.wave = wave_number
        self.alive = True
        self.oscillation_timer = random.uniform(0, math.pi * 2)
        self.shoot_timer = random.randint(60, 180)

        # Basic Syntax: Dictionaries for configuration
        stats = {
            "scout": {"hp": 30, "score": 100, "radius": 14, "color": COLOR_ORANGE, "speed": 1.4},
            "cruiser": {"hp": 75, "score": 250, "radius": 20, "color": COLOR_PURPLE, "speed": 0.9},
            "dreadnought": {"hp": 220, "score": 750, "radius": 32, "color": COLOR_RED, "speed": 0.5}
        }
        config = stats.get(enemy_type, stats["scout"])
        self.max_hp = config["hp"] + (wave_number - 1) * 15
        self.hp = self.max_hp
        self.score_value = config["score"]
        self.radius = config["radius"]
        self.color = config["color"]
        self.speed = config["speed"]

    def take_damage(self, amount: int) -> bool:
        """Applies damage. Returns True if destroyed."""
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def update(self, bullets: list):
        """Updates movement patterns and weapon firing."""
        self.y += self.speed
        self.oscillation_timer += 0.04
        
        # Sinuous horizontal motion
        amplitude = 25 if self.enemy_type == "scout" else 15
        self.x = self.original_x + math.sin(self.oscillation_timer) * amplitude

        # Out-of-bounds wrap-around or cleanup
        if self.y > SCREEN_HEIGHT + 40:
            self.y = -30
            self.original_x = random.uniform(50, SCREEN_WIDTH - 50)
            self.x = self.original_x

        # Enemy shooting logic
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot_timer = random.randint(120, 240)
            if self.enemy_type in ["cruiser", "dreadnought"] and self.y > 40:
                bullets.append(Bullet(self.x, self.y + self.radius, 4.5, is_player=False, color=COLOR_RED))
                if self.enemy_type == "dreadnought":
                    bullets.append(Bullet(self.x - 18, self.y + 10, 4.0, is_player=False, color=COLOR_ORANGE))
                    bullets.append(Bullet(self.x + 18, self.y + 10, 4.0, is_player=False, color=COLOR_ORANGE))

    def draw(self, surface: pygame.Surface):
        if not self.alive:
            return

        # Draw ship based on hierarchy
        if self.enemy_type == "scout":
            # Fast triangle dart
            pts = [(self.x, self.y + 14), (self.x - 12, self.y - 12), (self.x + 12, self.y - 12)]
            pygame.draw.polygon(surface, self.color, pts)
            pygame.draw.polygon(surface, COLOR_YELLOW, pts, width=1)
        elif self.enemy_type == "cruiser":
            # Heavy hexagon cruiser
            pts = [
                (self.x, self.y + 18),
                (self.x - 16, self.y + 4),
                (self.x - 12, self.y - 14),
                (self.x + 12, self.y - 14),
                (self.x + 16, self.y + 4)
            ]
            pygame.draw.polygon(surface, (40, 15, 60), pts)
            pygame.draw.polygon(surface, self.color, pts, width=2)
            pygame.draw.circle(surface, COLOR_CYAN, (int(self.x), int(self.y)), 4)
        else:
            # Massive dreadnought command ship
            pts = [
                (self.x, self.y + 26),
                (self.x - 28, self.y - 10),
                (self.x - 16, self.y - 24),
                (self.x + 16, self.y - 24),
                (self.x + 28, self.y - 10)
            ]
            pygame.draw.polygon(surface, (60, 20, 20), pts)
            pygame.draw.polygon(surface, self.color, pts, width=2)
            pygame.draw.circle(surface, COLOR_YELLOW, (int(self.x), int(self.y)), 6)

        # Health bar if damaged
        if self.hp < self.max_hp:
            bar_w = int(self.radius * 1.8)
            bar_h = 4
            health_w = int((self.hp / self.max_hp) * bar_w)
            bx = int(self.x - bar_w / 2)
            by = int(self.y - self.radius - 8)
            pygame.draw.rect(surface, (100, 20, 20), (bx, by, bar_w, bar_h))
            pygame.draw.rect(surface, COLOR_NEON_GREEN, (bx, by, health_w, bar_h))


# ==============================================================================
# SECTION 5: GAME ENGINE & STATE MANAGEMENT (Loops, Conditions, Syntax)
# ==============================================================================

class Game:
    """Core Game Engine orchestrating loops, recursion, entities, and HUD."""
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cosmic Vanguard: Void Recursion")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font_large = pygame.font.SysFont("Consolas", 36, bold=True)
        self.font_mid   = pygame.font.SysFont("Consolas", 20, bold=True)
        self.font_small = pygame.font.SysFont("Consolas", 14)

        self.sound_mgr = SoundManager()
        
        # Parallax Background Stars (Basic Syntax: List Comprehension & Loop)
        self.stars = [Star(SCREEN_WIDTH, SCREEN_HEIGHT) for _ in range(120)]
        
        # Pre-generate Fractal Nebulae using Recursion Concept #4
        self.nebula_nodes = []
        generate_fractal_nebula_recursive(200, 250, 70, 3, self.nebula_nodes)
        generate_fractal_nebula_recursive(600, 480, 80, 3, self.nebula_nodes)

        # Game State Variables
        self.state = "MENU"  # "MENU", "PLAYING", "GAMEOVER", "WAVE_CLEARED"
        self.score = 0
        self.high_score = 0
        self.wave = 1
        self.combo_streak = 0
        self.combo_timer = 0
        self.max_combo_timer = 150  # Frames before combo drops
        self.chain_reaction_records = 0
        self.screen_shake = 0
        self.show_help_overlay = False

        # Entity Collections (Basic Syntax: Lists)
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 90)
        self.player_bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.particles = []
        self.floating_texts = []
        self.powerups = []
        
        # Alien decoded message (Recursion Concept #5)
        self.alien_cipher = "NOISRUCER_FO_REWOP_EHT_HGUORHT_SSENKRAD_TAEFED"
        self.decoded_transmission = decode_alien_cipher_recursive(self.alien_cipher)

    def start_new_game(self):
        """Resets all metrics and spawns the initial recursive formation."""
        self.score = 0
        self.wave = 1
        self.combo_streak = 0
        self.chain_reaction_records = 0
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 90)
        self.player_bullets.clear()
        self.enemy_bullets.clear()
        self.particles.clear()
        self.floating_texts.clear()
        self.powerups.clear()
        self.spawn_wave()
        self.state = "PLAYING"

    def spawn_wave(self):
        """
        Spawns an alien fleet using RECURSION CONCEPT #1:
        Hierarchical fleet branching with depth determined by the wave count!
        """
        self.enemies.clear()
        self.player_bullets.clear()
        self.enemy_bullets.clear()

        # Depth scales from 1 up to 3 based on wave
        formation_depth = min(3, 1 + (self.wave // 2))
        center_x = SCREEN_WIDTH / 2
        center_y = 90
        spread_x = 90 + self.wave * 10
        spread_y = 50 + self.wave * 5

        # RECURSIVE INVOCATION
        self.enemies = generate_formation_recursive(
            cx=center_x,
            cy=center_y,
            depth=formation_depth,
            spread_x=spread_x,
            spread_y=spread_y,
            wave_number=self.wave
        )

        msg = f"WAVE {self.wave}: FLEET RECURSION LEVEL {formation_depth}"
        self.floating_texts.append(FloatingText(SCREEN_WIDTH / 2, 220, msg, COLOR_YELLOW, self.font_mid))

    def trigger_player_emp_shockwave(self):
        """
        Fires the Player's EMP Bomb, triggering RECURSION CONCEPT #2:
        Recursive chain reaction blast damage!
        """
        if self.player.emp_charges <= 0:
            return

        self.player.emp_charges -= 1
        self.sound_mgr.play("emp")
        self.screen_shake = 18

        # Create massive circular visual shockwave
        for angle in range(0, 360, 10):
            rad = math.radians(angle)
            px = self.player.x + math.cos(rad) * 40
            py = self.player.y + math.sin(rad) * 40
            self.particles.append(Particle(px, py, COLOR_CYAN, speed_scale=4.0))

        # RECURSIVE CHAIN REACTION CALL
        # Propagates through all nearby enemies up to depth 4
        eliminated_count = trigger_chain_reaction_recursive(
            origin_x=self.player.x,
            origin_y=self.player.y,
            radius=220,
            depth=4,
            enemies_list=self.enemies,
            particles_list=self.particles,
            sound_mgr=self.sound_mgr,
            decay_factor=0.85
        )

        if eliminated_count > 0:
            self.combo_streak += eliminated_count
            self.combo_timer = self.max_combo_timer
            # RECURSION CONCEPT #3: Recursive score bonus
            bonus_score = calc_combo_score_recursive(eliminated_count, base_points=150)
            self.score += bonus_score
            self.chain_reaction_records = max(self.chain_reaction_records, eliminated_count)
            
            banner = f"RECURSIVE CASCADE x{eliminated_count}! +{bonus_score} PTS"
            self.floating_texts.append(FloatingText(self.player.x, self.player.y - 40, banner, COLOR_HOT_PINK, self.font_mid))

    def process_collisions(self):
        """
        NESTED BASIC LOOPS:
        Examines collisions between Bullets, Enemies, Player, and Power-ups.
        """
        # 1. Player Bullets vs Enemies
        # BASIC LOOPS: Nested for-loops for pairwise collision testing
        for bullet in self.player_bullets:
            if not bullet.alive:
                continue
            for enemy in self.enemies:
                if not enemy.alive:
                    continue
                dist = math.hypot(bullet.x - enemy.x, bullet.y - enemy.y)
                if dist < (enemy.radius + 6):
                    bullet.alive = False
                    killed = enemy.take_damage(35)
                    
                    # Spark particles
                    for _ in range(5):
                        self.particles.append(Particle(bullet.x, bullet.y, COLOR_YELLOW, speed_scale=1.5))

                    if killed:
                        self.sound_mgr.play("explosion")
                        self.screen_shake = 6
                        for _ in range(14):
                            self.particles.append(Particle(enemy.x, enemy.y, enemy.color, speed_scale=2.8))

                        # Combo scoring
                        self.combo_streak += 1
                        self.combo_timer = self.max_combo_timer
                        # RECURSION CONCEPT #3: Calculate combo bonus score
                        awarded_score = calc_combo_score_recursive(self.combo_streak, enemy.score_value)
                        self.score += awarded_score

                        # Floating score text
                        msg = f"+{awarded_score}" if self.combo_streak <= 1 else f"+{awarded_score} (x{self.combo_streak} COMBO!)"
                        col = COLOR_WHITE if self.combo_streak <= 1 else COLOR_YELLOW
                        self.floating_texts.append(FloatingText(enemy.x, enemy.y, msg, col, self.font_small))

                        # Build EMP Charge
                        self.player.emp_charge_progress += 20
                        if self.player.emp_charge_progress >= 100:
                            self.player.emp_charge_progress = 0
                            if self.player.emp_charges < self.player.max_emp_charges:
                                self.player.emp_charges += 1
                                self.sound_mgr.play("powerup")
                                self.floating_texts.append(FloatingText(self.player.x, self.player.y - 30, "EMP BOMB READY!", COLOR_CYAN, self.font_mid))

                        # Chance to drop power-ups from cruisers & dreadnoughts
                        if enemy.enemy_type in ["cruiser", "dreadnought"] and random.random() < 0.45:
                            p_type = random.choice(["shield", "rapid", "bomb"])
                            self.powerups.append(PowerUp(enemy.x, enemy.y, p_type))
                    break  # Stop checking this bullet against other enemies

        # 2. Enemy Bullets vs Player
        for bullet in self.enemy_bullets:
            if not bullet.alive:
                continue
            dist = math.hypot(bullet.x - self.player.x, bullet.y - self.player.y)
            if dist < (self.player.width / 2 + 3):
                bullet.alive = False
                destroyed = self.player.take_damage(20, self.sound_mgr)
                self.combo_streak = 0  # Combo lost on hit!
                self.screen_shake = 10
                for _ in range(10):
                    self.particles.append(Particle(self.player.x, self.player.y, COLOR_RED, speed_scale=2.2))
                if destroyed and self.player.lives <= 0:
                    self.state = "GAMEOVER"

        # 3. Enemy Ship Body vs Player
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            dist = math.hypot(enemy.x - self.player.x, enemy.y - self.player.y)
            if dist < (enemy.radius + self.player.width / 2):
                enemy.take_damage(100)
                destroyed = self.player.take_damage(40, self.sound_mgr)
                self.combo_streak = 0
                self.screen_shake = 14
                if destroyed and self.player.lives <= 0:
                    self.state = "GAMEOVER"

        # 4. Power-ups vs Player
        for pup in self.powerups:
            if not pup.alive:
                continue
            dist = math.hypot(pup.x - self.player.x, pup.y - self.player.y)
            if dist < (self.player.width / 2 + 15):
                pup.alive = False
                self.sound_mgr.play("powerup")
                if pup.p_type == "shield":
                    self.player.health = min(self.player.max_health, self.player.health + 40)
                    self.floating_texts.append(FloatingText(self.player.x, self.player.y - 25, "SHIELD REPAIRED!", COLOR_NEON_GREEN, self.font_small))
                elif pup.p_type == "rapid":
                    self.player.rapid_fire_timer = 360  # 6 seconds of rapid fire
                    self.floating_texts.append(FloatingText(self.player.x, self.player.y - 25, "RAPID OVERCHARGE!", COLOR_YELLOW, self.font_small))
                elif pup.p_type == "bomb":
                    self.player.emp_charges = min(self.player.max_emp_charges, self.player.emp_charges + 1)
                    self.floating_texts.append(FloatingText(self.player.x, self.player.y - 25, "+1 EMP BOMB!", COLOR_PURPLE, self.font_small))

    def update(self):
        """
        BASIC LOOPS:
        Entity list updates and state transitions.
        """
        # Update Parallax Starfield
        for star in self.stars:
            star.update()

        if self.state != "PLAYING":
            return

        # Screen shake decay
        if self.screen_shake > 0:
            self.screen_shake -= 1

        # Combo timer decay
        if self.combo_timer > 0:
            self.combo_timer -= 1
            if self.combo_timer == 0:
                self.combo_streak = 0  # Streak expired

        # Player update
        self.player.update()

        # Update lists using BASIC LOOPS & LIST COMPREHENSIONS (Basic Syntax)
        for bullet in self.player_bullets:
            bullet.update()
        for bullet in self.enemy_bullets:
            bullet.update()
        for enemy in self.enemies:
            enemy.update(self.enemy_bullets)
        for pup in self.powerups:
            pup.update()

        # Update particles (removing dead ones via list comprehension)
        self.particles = [p for p in self.particles if p.update()]
        self.floating_texts = [ft for ft in self.floating_texts if ft.update()]

        # Filter out dead bullets and dead powerups
        self.player_bullets = [b for b in self.player_bullets if b.alive]
        self.enemy_bullets  = [b for b in self.enemy_bullets if b.alive]
        self.powerups       = [p for p in self.powerups if p.alive]

        # Collision resolutions
        self.process_collisions()

        # Check wave completion
        alive_enemies = [e for e in self.enemies if e.alive]
        if len(alive_enemies) == 0:
            self.wave += 1
            self.sound_mgr.play("powerup")
            self.spawn_wave()

        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score

    def draw_hud(self, surface: pygame.Surface):
        """Renders HUD showing score, combo multipliers, health, and recursion indicators."""
        # Top HUD banner
        hud_bar = pygame.Surface((SCREEN_WIDTH, 48), pygame.SRCALPHA)
        hud_bar.fill(COLOR_HUD_BG)
        surface.blit(hud_bar, (0, 0))

        # Basic Syntax: f-strings for formatted output
        score_txt = self.font_mid.render(f"SCORE: {self.score:06d}", True, COLOR_CYAN)
        surface.blit(score_txt, (15, 12))

        high_txt = self.font_small.render(f"HIGH: {self.high_score:06d}", True, COLOR_YELLOW)
        surface.blit(high_txt, (210, 16))

        wave_txt = self.font_mid.render(f"WAVE: {self.wave}", True, COLOR_HOT_PINK)
        surface.blit(wave_txt, (350, 12))

        # Combo display with progress bar
        if self.combo_streak > 1:
            combo_str = f"COMBO x{self.combo_streak}!"
            combo_surf = self.font_mid.render(combo_str, True, COLOR_YELLOW)
            surface.blit(combo_surf, (480, 12))
            # Combo timer bar
            bar_w = int(60 * (self.combo_timer / self.max_combo_timer))
            pygame.draw.rect(surface, COLOR_YELLOW, (480, 34, bar_w, 4))

        # Lives display
        lives_txt = self.font_mid.render(f"LIVES: {'A ' * self.player.lives}", True, COLOR_WHITE)
        surface.blit(lives_txt, (SCREEN_WIDTH - 150, 12))

        # Bottom HUD: Player Health Bar & EMP Status
        bottom_y = SCREEN_HEIGHT - 32
        
        # Health Bar
        hp_pct = max(0.0, self.player.health / self.player.max_health)
        pygame.draw.rect(surface, (80, 20, 20), (15, bottom_y, 160, 18), border_radius=3)
        hp_color = COLOR_NEON_GREEN if hp_pct > 0.4 else COLOR_RED
        pygame.draw.rect(surface, hp_color, (15, bottom_y, int(160 * hp_pct), 18), border_radius=3)
        hp_lbl = self.font_small.render(f"SHIELD {int(hp_pct * 100)}%", True, COLOR_WHITE)
        surface.blit(hp_lbl, (20, bottom_y + 2))

        # EMP Bombs Ready Indicator
        emp_status = f"EMP BOMBS [B]: {self.player.emp_charges}/{self.player.max_emp_charges}"
        emp_col = COLOR_CYAN if self.player.emp_charges > 0 else (120, 120, 120)
        emp_lbl = self.font_small.render(emp_status, True, emp_col)
        surface.blit(emp_lbl, (200, bottom_y + 2))

        # Controls & Help hint
        hint_lbl = self.font_small.render("[H] Toggle Concepts & Help", True, (160, 160, 190))
        surface.blit(hint_lbl, (SCREEN_WIDTH - 230, bottom_y + 2))

    def draw_help_overlay(self, surface: pygame.Surface):
        """Displays overlay explaining how loops and recursion are used in real-time."""
        overlay = pygame.Surface((SCREEN_WIDTH - 80, SCREEN_HEIGHT - 120))
        overlay.fill((12, 16, 32))
        overlay.set_alpha(245)
        rect = overlay.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        # Border
        pygame.draw.rect(overlay, COLOR_CYAN, overlay.get_rect(), width=2)
        
        lines = [
            ("=== PYTHON SYNTAX & RECURSION GUIDE ===", COLOR_YELLOW, True),
            ("", COLOR_WHITE, False),
            ("1. RECURSIVE SQUADRON GENERATION (generate_formation_recursive):", COLOR_HOT_PINK, True),
            ("   - Base Case: depth == 0 -> Spawns vanguard scout drone.", COLOR_WHITE, False),
            ("   - Recursive Step: Spawns commander, then recursively spawns", COLOR_WHITE, False),
            ("     left wing (depth-1) and right wing (depth-1).", COLOR_WHITE, False),
            ("", COLOR_WHITE, False),
            ("2. RECURSIVE CHAIN REACTION EXPLOSIONS (trigger_chain_reaction_recursive):", COLOR_HOT_PINK, True),
            ("   - Press [B] to trigger EMP! Destroys nearby ships.", COLOR_WHITE, False),
            ("   - Each destroyed ship cascades into its own child blast (depth-1).", COLOR_WHITE, False),
            ("", COLOR_WHITE, False),
            ("3. RECURSIVE COMBO SCORING (calc_combo_score_recursive):", COLOR_HOT_PINK, True),
            ("   - Recurrence relation compounds points for consecutive streaks.", COLOR_WHITE, False),
            ("", COLOR_WHITE, False),
            ("4. BASIC LOOPS IMPLEMENTED:", COLOR_CYAN, True),
            ("   - while running: Primary 60FPS Game Loop.", COLOR_WHITE, False),
            ("   - for bullet in bullets / for enemy in enemies: Nested collision checks.", COLOR_WHITE, False),
            ("   - for star in stars: Parallax 3D space movement.", COLOR_WHITE, False),
            ("   - [p for p in particles if p.update()]: List comprehension filtering.", COLOR_WHITE, False),
            ("", COLOR_WHITE, False),
            ("CONTROLS: [WASD / Arrows] Move | [Space] Fire | [B] EMP Shockwave", COLOR_NEON_GREEN, True),
            ("Press [H] to close this concepts overlay.", COLOR_YELLOW, False)
        ]

        y_offset = 20
        # BASIC LOOP: Iterating over lines to render documentation text
        for text, color, bold in lines:
            f = self.font_small if not bold else self.font_mid
            rendered = f.render(text, True, color)
            overlay.blit(rendered, (25, y_offset))
            y_offset += 21

        surface.blit(overlay, rect.topleft)

    def draw(self):
        """Main rendering pass executing layered draw loops."""
        # Calculate screen shake offset
        ox = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        oy = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        
        # Clear background
        self.screen.fill(COLOR_BLACK)

        # 1. Draw Fractal Nebulae (Pre-computed via Recursion)
        for node in self.nebula_nodes:
            # Draw subtle glowing aura
            surf = pygame.Surface((int(node["radius"] * 2), int(node["radius"] * 2)), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*node["color"], node["alpha"]), 
                               (int(node["radius"]), int(node["radius"])), int(node["radius"]))
            self.screen.blit(surf, (int(node["x"] - node["radius"] + ox), int(node["y"] - node["radius"] + oy)))

        # 2. Draw Stars (BASIC LOOP: for star in stars)
        for star in self.stars:
            star.draw(self.screen)

        # Render Game Entities
        if self.state in ["PLAYING", "GAMEOVER"]:
            # Draw Power-ups
            for pup in self.powerups:
                pup.draw(self.screen)

            # Draw Bullets (BASIC LOOP: for bullet in bullets)
            for bullet in self.player_bullets:
                bullet.draw(self.screen)
            for bullet in self.enemy_bullets:
                bullet.draw(self.screen)

            # Draw Enemies
            for enemy in self.enemies:
                enemy.draw(self.screen)

            # Draw Player
            self.player.draw(self.screen)

            # Draw Particles
            for p in self.particles:
                p.draw(self.screen)

            # Draw Floating Text
            for ft in self.floating_texts:
                ft.draw(self.screen)

            # Draw HUD
            self.draw_hud(self.screen)

        # Screen Overlays (Menu / Game Over)
        if self.state == "MENU":
            self.draw_menu()
        elif self.state == "GAMEOVER":
            self.draw_game_over()

        # Help / Concept Walkthrough Overlay
        if self.show_help_overlay:
            self.draw_help_overlay(self.screen)

        pygame.display.flip()

    def draw_menu(self):
        """Renders Title Screen."""
        title = self.font_large.render("COSMIC VANGUARD", True, COLOR_CYAN)
        subtitle = self.font_mid.render("VOID RECURSION", True, COLOR_HOT_PINK)
        prompt = self.font_mid.render("PRESS [ENTER] OR [SPACE] TO ENGAGE", True, COLOR_YELLOW)
        hint = self.font_small.render("Press [H] during flight for Loop & Recursion Deep Dive", True, (180, 180, 210))

        # Decoded secret transmission easter egg (Recursion Concept #5)
        secret = self.font_small.render(f"Decoded Alien Signal: \"{self.decoded_transmission}\"", True, COLOR_NEON_GREEN)

        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 210)))
        self.screen.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH // 2, 260)))
        self.screen.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH // 2, 380)))
        self.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, 440)))
        self.screen.blit(secret, secret.get_rect(center=(SCREEN_WIDTH // 2, 520)))

    def draw_game_over(self):
        """Renders Game Over Screen."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((20, 0, 10, 180))
        self.screen.blit(overlay, (0, 0))

        title = self.font_large.render("SYSTEM CRITICAL: DEFEATED", True, COLOR_RED)
        score_info = self.font_mid.render(f"FINAL SCORE: {self.score}  |  WAVE REACHED: {self.wave}", True, COLOR_WHITE)
        chain_info = self.font_small.render(f"MAX RECURSIVE CHAIN REACTION: x{self.chain_reaction_records}", True, COLOR_HOT_PINK)
        retry = self.font_mid.render("PRESS [R] OR [ENTER] TO REBOOT", True, COLOR_YELLOW)

        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 240)))
        self.screen.blit(score_info, score_info.get_rect(center=(SCREEN_WIDTH // 2, 310)))
        self.screen.blit(chain_info, chain_info.get_rect(center=(SCREEN_WIDTH // 2, 350)))
        self.screen.blit(retry, retry.get_rect(center=(SCREEN_WIDTH // 2, 430)))

    def run(self):
        """
        THE MAIN GAME LOOP (Basic Loops Concept: while running)
        Executes at a rock-steady 60 FPS.
        """
        running = True
        
        # BASIC LOOP: Main Game Loop
        while running:
            # 1. Event Handling Loop (BASIC LOOP: for event in pygame.event.get())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_h:
                        # Toggle concept helper overlay
                        self.show_help_overlay = not self.show_help_overlay
                    elif self.state == "MENU":
                        if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                            self.start_new_game()
                    elif self.state == "PLAYING":
                        # Trigger recursive EMP Shockwave
                        if event.key == pygame.K_b:
                            self.trigger_player_emp_shockwave()
                    elif self.state == "GAMEOVER":
                        if event.key in [pygame.K_r, pygame.K_RETURN]:
                            self.start_new_game()

            # 2. Continuous Input Handling
            if self.state == "PLAYING":
                keys = pygame.key.get_pressed()
                self.player.handle_input(keys, self.player_bullets, self.sound_mgr, self.particles)

            # 3. Game Simulation Step
            self.update()

            # 4. Rendering Step
            self.draw()

            # 5. Cap framerate at 60 FPS
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


# ==============================================================================
# SECTION 6: ENTRY POINT (Basic Syntax: __name__ == '__main__')
# ==============================================================================
if __name__ == "__main__":
    game = Game()
    game.run()
