;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-abbr-reader.ss" "lang")((modname space-invaders-starter-personal-solutions) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(require 2htdp/universe)
(require 2htdp/image)

;; Space Invaders


;; Constants:

(define WIDTH  300)
(define HEIGHT 500)

(define INVADER-X-SPEED 1.5)  ;speeds (not velocities) in pixels per tick
(define INVADER-Y-SPEED 1.5)
(define TANK-SPEED 2)
(define MISSILE-SPEED 10)

(define HIT-RANGE 10)

(define INVADE-RATE 4)

(define MTS (empty-scene WIDTH HEIGHT))

(define INVADER
  (overlay/xy (ellipse 10 15 "outline" "blue")              ;cockpit cover
              -5 6
              (ellipse 20 10 "solid"   "blue")))            ;saucer

(define TANK
  (overlay/xy (overlay (ellipse 28 8 "solid" "black")       ;tread center
                       (ellipse 30 10 "solid" "green"))     ;tread outline
              5 -14
              (above (rectangle 5 10 "solid" "black")       ;gun
                     (rectangle 20 10 "solid" "black"))))   ;main body

(define TANK-HEIGHT/2 (/ (image-height TANK) 2))

(define MISSILE (ellipse 5 15 "solid" "red"))



;; Data Definitions:

(define-struct game (invaders missiles tank))
;; Game is (make-game  (listof Invader) (listof Missile) Tank)
;; interp. the current state of a space invaders game
;;         with the current invaders, missiles and tank position

;; Game constants defined below Missile data definition

#;
(define (fn-for-game g)
  (... (fn-for-loinvader (game-invaders g))
       (fn-for-lom (game-missiles g))
       (fn-for-tank (game-tank g))))



(define-struct tank (x dir))
;; Tank is (make-tank Number Integer[-1, 1])
;; interp. the tank location is x, HEIGHT - TANK-HEIGHT/2 in screen coordinates
;;         the tank moves TANK-SPEED pixels per clock tick left if dir -1, right if dir 1

(define T0 (make-tank (/ WIDTH 2) 1))   ;center going right
(define T1 (make-tank 50 1))            ;going right
(define T2 (make-tank 50 -1))           ;going left
(define T3 (make-tank WIDTH 1))         ;max right
(define T4 (make-tank 0 -1))            ;max left

#;
(define (fn-for-tank t)
  (... (tank-x t) (tank-dir t)))



(define-struct invader (x y dx))
;; Invader is (make-invader Number Number Number)
;; interp. the invader is at (x, y) in screen coordinates
;;         the invader moves along x by dx pixels per clock tick

(define I1 (make-invader 150 100 12))           ;not landed, moving right
(define I2 (make-invader 150 HEIGHT -10))       ;exactly landed, moving left
(define I3 (make-invader 150 (+ HEIGHT 10) 10)) ;> landed, moving right


#;
(define (fn-for-invader invader)
  (... (invader-x invader) (invader-y invader) (invader-dx invader)))

;; ListOfInvader is one of:
;; - empty
;; - (cons Invader ListOfInvader)

(define LOI0 empty)
(define LOI1 (cons I1 empty))
(define LOI2 (cons I2 LOI1))

#;
(define (fn-for-loi loi)
  (cond [(empty? loi) (...)]
        [else
         (... (first loi)
              (fn-for-loi (rest loi)))]))

(define-struct missile (x y))
;; Missile is (make-missile Number Number)
;; interp. the missile's location is x y in screen coordinates

(define M1 (make-missile 150 300))                       ;not hit U1
(define M2 (make-missile (invader-x I1) (+ (invader-y I1) 10)))  ;exactly hit U1
(define M3 (make-missile (invader-x I1) (+ (invader-y I1)  5)))  ;> hit U1

#;
(define (fn-for-missile m)
  (... (missile-x m) (missile-y m)))

;; ListOfMissile is one of:
;; - empty
;; - (cons Missile ListOfMissile)

(define LOM0 empty)
(define LOM1 (cons M1 empty))
(define LOM2 (cons (make-missile 100 100) LOM1))

#;
(define (fn-for-lom lom)
  (cond [(empty? lom) (...)]
        [else
         (... (first lom)
              (fn-for-lom (rest lom)))]))


(define G0 (make-game empty empty T0))
(define G1 (make-game empty empty T1))
(define G2 (make-game (list I1) (list M1) T1))
(define G3 (make-game (list I1 I2) (list M1 M2) T1))

;; Functions:
;; ==========

;; G -> G
;; start the world with (main G0)
;; 
(define (main g)
  (big-bang g                   ; G
    (on-tick   tock)     ; G -> G
    (to-draw   render)   ; G -> Image
    (stop-when stop)      ; G -> Boolean
    (on-key    press)))    ; G KeyEvent -> G

;; G -> G
;; produce the next list of missiles, list of invaders, and tank
;; Tank Tests
;(check-expect (tock G0) (make-game empty empty (make-tank (+ (/ WIDTH 2) (* 1 TANK-SPEED)) 1)))
;(check-expect (tock (make-game empty empty T2)) (make-game empty empty (make-tank (+ 50 (* -1 TANK-SPEED)) -1)))
;(check-expect (tock (make-game empty empty T3)) (make-game empty empty (make-tank WIDTH 1)))
;(check-expect (tock (make-game empty empty T4)) (make-game empty empty (make-tank 0 -1)))

#;
(define (tock g) G0) ;stub

(define (tock g)
  (make-game
   (move-invaders (collide-invaders (create-invaders (game-invaders g)) (game-missiles g)))
   (move-missiles (collide-missiles (game-invaders g) (filter-missiles (game-missiles g))))
   (move-tank (game-tank g))))

;; ListOfInvaders ListofMissiles -> ListOfInvaders
;; Checks a list of invaders against a list of missiles and removes invaders that have collided with missiles
(check-expect (collide-invaders LOI0 LOM0) LOI0)
(check-expect (collide-invaders LOI1 LOM1) LOI1)
(check-expect (collide-invaders (list (make-invader 150 100 10)) (list (make-missile 150 100))) empty)
(check-expect (collide-invaders (list (make-invader 150 100 10)) (list (make-missile 150 95))) empty)
(check-expect (collide-invaders (list (make-invader 150 100 10)) (list (make-missile 150 105))) empty)
(check-expect (collide-invaders (list (make-invader 150 100 10)) (list (make-missile 150 90))) (list (make-invader 150 100 10)))
(check-expect (collide-invaders (list (make-invader 150 100 10)) (list (make-missile 150 110))) (list (make-invader 150 100 10)))
(check-expect (collide-invaders (list (make-invader 150 100 10)) (list (make-missile 145 100))) empty)
(check-expect (collide-invaders (list (make-invader 150 100 10)) (list (make-missile 155 100))) empty)
(check-expect (collide-invaders (list (make-invader 150 100 10)) (list (make-missile 140 100))) (list (make-invader 150 100 10)))
(check-expect (collide-invaders (list (make-invader 150 100 10)) (list (make-missile 160 100))) (list (make-invader 150 100 10)))
(check-expect (collide-invaders (list (make-invader 150 100 10)) (list (make-missile 155 105))) empty)
(check-expect (collide-invaders (list (make-invader 150 100 10)) (list (make-missile 145 95))) empty)

;(define (collide-invaders loi lom) LOI0) ;stub

(define (collide-invaders loi lom)
  (cond [(empty? loi) empty]
        [else
         (cond [(collide-invader (first loi) lom) (collide-invaders (rest loi) lom)]
               [else
                (cons (first loi) (collide-invaders (rest loi) lom))])]))

;; Invader ListOfMissiles -> Boolean
;; Checks one invader against a list of missiles to see if there is a collision and returns true if so
(check-expect (collide-invader (make-invader 150 100 10) (list (make-missile 150 100))) true)
(check-expect (collide-invader (make-invader 150 100 10) (list (make-missile 155 105))) true)
(check-expect (collide-invader (make-invader 150 100 10) (list (make-missile 140 100))) false)
(check-expect (collide-invader (make-invader 150 100 10) (list (make-missile 150 110))) false)

;(define (collide-invader i lom) true) ;stub

(define (collide-invader i lom)
  (cond [(empty? lom) false]
        [else
         (cond [(and (< (- (invader-x i) HIT-RANGE) (missile-x (first lom)) (+ (invader-x i) HIT-RANGE))
                     (< (- (invader-y i) HIT-RANGE) (missile-y (first lom)) (+ (invader-y i) HIT-RANGE)))
                true]
               [else
                (collide-invader i (rest lom))])]))

;; ListOfInvaders ListofMissiles -> ListOfMissiles
;; Checks a list of invaders against a list of missiles and removes missiles that have collided with invaders
(check-expect (collide-missiles LOI0 LOM0) LOM0)
(check-expect (collide-missiles LOI1 LOM1) LOM1)
(check-expect (collide-missiles (list (make-invader 150 100 10)) (list (make-missile 150 100))) empty)
(check-expect (collide-missiles (list (make-invader 150 100 10)) (list (make-missile 150 95))) empty)
(check-expect (collide-missiles (list (make-invader 150 100 10)) (list (make-missile 150 105))) empty)
(check-expect (collide-missiles (list (make-invader 150 100 10)) (list (make-missile 150 90))) (list (make-missile 150 90)))
(check-expect (collide-missiles (list (make-invader 150 100 10)) (list (make-missile 150 110))) (list (make-missile 150 110)))
(check-expect (collide-missiles (list (make-invader 150 100 10)) (list (make-missile 145 100))) empty)
(check-expect (collide-missiles (list (make-invader 150 100 10)) (list (make-missile 155 100))) empty)
(check-expect (collide-missiles (list (make-invader 150 100 10)) (list (make-missile 140 100))) (list (make-missile 140 100)))
(check-expect (collide-missiles (list (make-invader 150 100 10)) (list (make-missile 160 100))) (list (make-missile 160 100)))
(check-expect (collide-missiles (list (make-invader 150 100 10)) (list (make-missile 155 105))) empty)
(check-expect (collide-missiles (list (make-invader 150 100 10)) (list (make-missile 145 95))) empty)

;(define (collide-missiles loi lom) LOM0) ;stub

(define (collide-missiles loi lom)
  (cond [(empty? lom) empty]
        [else
         (cond [(collide-missile (first lom) loi) (collide-missiles loi (rest lom))]
               [else
                (cons (first lom) (collide-missiles loi (rest lom)))])]))

;; Missile ListofInvaders -> Boolean
;; Checks one missile against a list of invaders to see if there is a collision and retuns true if so
(check-expect (collide-missile (make-missile 150 100) (list (make-invader 150 100 10))) true)
(check-expect (collide-missile (make-missile 150 100) (list (make-invader 155 105 10))) true)
(check-expect (collide-missile (make-missile 150 100) (list (make-invader 160 100 10))) false)
(check-expect (collide-missile (make-missile 150 100) (list (make-invader 150 110 10))) false)

;(define (collide-missile m loi) true) ;stub

(define (collide-missile m loi)
  (cond [(empty? loi) false]
        [else
         (cond [(and (< (- (missile-x m) HIT-RANGE) (invader-x (first loi)) (+ (missile-x m) HIT-RANGE))
                     (< (- (missile-y m) HIT-RANGE) (invader-y (first loi)) (+ (missile-y m) HIT-RANGE)))
                true]
               [else
                (collide-missile m (rest loi))])]))


;; ListOfInvaders -> ListOfInvaders
;; Adds a new invader to the current ListOfInvaders
;; NOTE: Tests commented due to random spawning mechanics
;; (check-expect (create-invaders LOI0) (cons (make-invader (/ WIDTH 2) 0 INVADER-X-SPEED) empty))
;; (check-expect (create-invaders LOI1) (cons (make-invader (/ WIDTH 2) 0 INVADER-X-SPEED) LOI1))

;(define (create-invaders loi) LOI0) ;stub

(define (create-invaders loi)
  (if (< (random 100) INVADE-RATE)
      (cond [(empty? loi) (cons (make-invader (random (+ 1 WIDTH)) 0 INVADER-X-SPEED) empty)]
            [else
             (cons (make-invader (random (+ 1 WIDTH)) 0 INVADER-X-SPEED) loi)])
      loi))

;; ListOfInvaders -> ListOfInvaders
;; Moves invaders horizontally and down to their new x and y positions respectively
(check-expect (move-invaders LOI0) empty)
(check-expect (move-invaders LOI1)
              (cons (make-invader (+ 150 12) (+ 100 INVADER-Y-SPEED) 12) empty))
(check-expect (move-invaders LOI2)
              (cons (make-invader (- 150 10) (+ HEIGHT INVADER-Y-SPEED) -10) (cons (make-invader (+ 150 12) (+ 100 INVADER-Y-SPEED) 12) empty)))
(check-expect (move-invaders (cons (make-invader 100 100 10) (cons (make-invader WIDTH 100  10) empty)))
              (cons (make-invader 110 (+ 100 INVADER-Y-SPEED) 10) (cons (make-invader WIDTH (+ 100 INVADER-Y-SPEED) -10) empty)))
(check-expect (move-invaders (cons (make-invader 100 100 10) (cons (make-invader     0 100 -10) empty)))
              (cons (make-invader 110 (+ 100 INVADER-Y-SPEED) 10) (cons (make-invader 0 (+ 100 INVADER-Y-SPEED) 10) empty)))

;(define (move-invaders loi) LOI0) ;stub

(define (move-invaders loi)
  (cond [(empty? loi) empty]
        [else
         (cond [(> (+ (invader-x (first loi)) (invader-dx (first loi))) WIDTH)
                (cons (make-invader WIDTH (+ (invader-y (first loi)) INVADER-Y-SPEED) (- (invader-dx (first loi)))) (move-invaders (rest loi)))]
               [(< (+ (invader-x (first loi)) (invader-dx (first loi)))     0)
                (cons (make-invader     0 (+ (invader-y (first loi)) INVADER-Y-SPEED) (- (invader-dx (first loi)))) (move-invaders (rest loi)))]
               [else
                (cons (make-invader (+ (invader-x (first loi)) (invader-dx (first loi))) (+ (invader-y (first loi)) INVADER-Y-SPEED) (invader-dx (first loi)))
                      (move-invaders (rest loi)))])]))

;; ListOfMissiles -> ListOfMissiles
;; removes missiles from list if they are out of the playing field
(check-expect (filter-missiles LOM0) LOM0)
(check-expect (filter-missiles LOM1) LOM1)
(check-expect (filter-missiles (cons (make-missile 100 1) LOM1)) (cons (make-missile 100 1) LOM1))
(check-expect (filter-missiles (cons (make-missile 100 0) LOM1)) (cons (make-missile 100 0) LOM1))
(check-expect (filter-missiles (cons (make-missile 100 -1) LOM1)) LOM1)
(check-expect (filter-missiles (cons (make-missile 100 100) (cons (make-missile 100 -1) empty))) (cons (make-missile 100 100) empty))

;(define (filter-missiles lom) LOM0) ;stub

(define (filter-missiles lom)
  (cond [(empty? lom) empty]
        [else
         (if (< (missile-y (first lom)) 0)
             (filter-missiles (rest lom))
             (cons (first lom) (filter-missiles (rest lom))))]))

;; ListOfMissiles -> ListOfMissiles
;; Moves missiles up vertically the appropriate distance per tick
(check-expect (move-missiles LOM0) empty)
(check-expect (move-missiles LOM1) (cons (make-missile 150 (- 300 MISSILE-SPEED)) empty))
(check-expect (move-missiles LOM2) (cons (make-missile 100 (- 100 MISSILE-SPEED)) (cons (make-missile 150 (- 300 MISSILE-SPEED)) empty)))

;(define (move-missiles lom) LOM0) ;stub

(define (move-missiles lom)
  (cond [(empty? lom) empty]
        [else
         (cons (make-missile (missile-x (first lom)) (- (missile-y (first lom)) MISSILE-SPEED))
               (move-missiles (rest lom)))]))

;; Tank -> Tank
;; Moves tank in the direction assigned assuming room left to move
(check-expect (move-tank T0) (make-tank (+ (/ WIDTH 2) (* 1 TANK-SPEED)) 1))
(check-expect (move-tank T1) (make-tank (+ 50 (* 1 TANK-SPEED)) 1))
(check-expect (move-tank T2) (make-tank (+ 50 (* -1 TANK-SPEED)) -1))
(check-expect (move-tank T3) (make-tank WIDTH 1))
(check-expect (move-tank T4) (make-tank 0 -1))

;(define (move-tank t) T0) ;stub

(define (move-tank t)
  (cond [(> (+ (tank-x t) (* (tank-dir t) TANK-SPEED)) WIDTH) (make-tank WIDTH 1)]
        [(< (+ (tank-x t) (* (tank-dir t) TANK-SPEED))     0) (make-tank 0    -1)]
        [else
         (make-tank (+ (tank-x t) (* (tank-dir t) TANK-SPEED)) (tank-dir t))]))


;; G -> Image
;; render the of the MTS, the tank, the invaders, the missiles 
(check-expect (render G0) (place-image TANK (/ WIDTH 2) (- HEIGHT TANK-HEIGHT/2) MTS))
(check-expect (render G2) (place-image MISSILE 150 300
                                       (place-image INVADER 150 100
                                                    (place-image TANK 50 (- HEIGHT TANK-HEIGHT/2) MTS))))
(check-expect (render G3) (place-image MISSILE 150 300
                                       (place-image MISSILE 150 110
                                                    (place-image INVADER 150 100
                                                                 (place-image INVADER 150 HEIGHT
                                                                              (place-image TANK 50 (- HEIGHT TANK-HEIGHT/2) MTS))))))

;(define (render g) (square 0 "solid" "white")) ;stub

(define (render g)
  (render-missiles (game-missiles g)
                   (render-invaders (game-invaders g)
                                    (render-tank (game-tank g)))))

;; ListOfMissiles Image -> Image
;; render a list of missiles in their respective positions on an imasge with invaders and the tank
(check-expect (render-missiles LOM0 (render-invaders LOI0 (render-tank T0))) (render-tank T0))
(check-expect (render-missiles LOM2 (render-invaders LOI2 (render-tank T0))) (place-image MISSILE 100 100
                                                                                          (place-image MISSILE 150 300
                                                                                                       (render-invaders LOI2 (render-tank T0)))))

;(define (render-missiles lom img) (square 0 "solid" "white")) ;stub

(define (render-missiles lom img)
  (cond [(empty? lom) img]
        [else
         (place-image MISSILE (missile-x (first lom)) (missile-y (first lom))
                      (render-missiles (rest lom) img))]))

;; ListOfInvaders Image -> Image
;; renders a list of invaders in their respective positions on an image with the tank
(check-expect (render-invaders LOI0 (render-tank T0)) (render-tank T0))
(check-expect (render-invaders LOI2 (render-tank T0)) (place-image INVADER 150 100
                                                                   (place-image INVADER 150 HEIGHT
                                                                                (render-tank T0))))

;(define (render-invaders loi img) (square 0 "solid" "white")) ;stub

(define (render-invaders loi img)
  (cond [(empty? loi) img]
        [else
         (place-image INVADER (invader-x (first loi)) (invader-y (first loi))
                      (render-invaders (rest loi) img))]))

;; Tank -> Image
;; renders the position of the tank as a picture on an empty scene
(check-expect (render-tank T0) (place-image TANK (/ WIDTH 2) (- HEIGHT TANK-HEIGHT/2) MTS))

;(define (render-tank t) (square 0 "solid" "white")) ;stub

(define (render-tank t) (place-image TANK (tank-x t) (- HEIGHT TANK-HEIGHT/2) MTS))

;; G KeyEvent -> G
;; produce a new missile
(check-expect (press G0 "a") G0)
(check-expect (press G0 "left") (make-game empty empty (make-tank (/ WIDTH 2) -1)))
(check-expect (press G0 "right") (make-game empty empty (make-tank (/ WIDTH 2) 1)))
(check-expect (press G0 " ") (make-game (game-invaders G0) (cons (make-missile (tank-x (game-tank G0)) (- HEIGHT (image-height TANK))) empty) (game-tank G0)))
(check-expect (press G2 " ") (make-game (game-invaders G2) (cons (make-missile (tank-x (game-tank G2)) (- HEIGHT (image-height TANK))) (game-missiles G2)) (game-tank G2)))

;(define (press g ke) G0) ;stub

(define (press g ke)
  (cond [(key=? ke " ")
         (make-game (game-invaders g) (create-missile (game-missiles g) (game-tank g)) (game-tank g))]
        [(key=? ke "left")
         (make-game (game-invaders g) (game-missiles g) (make-tank (tank-x (game-tank g)) -1 ))]
        [(key=? ke "right")
         (make-game (game-invaders g) (game-missiles g) (make-tank (tank-x (game-tank g))  1 ))]
        [else 
         g]))

;; ListOfMissle Tank -> ListOfMissle
;; Adds a missile to the list of missles
(check-expect (create-missile empty T0) (cons (make-missile (tank-x T0) (- HEIGHT (image-height TANK))) empty))
(check-expect (create-missile LOM2 T1) (cons (make-missile (tank-x T1) (- HEIGHT (image-height TANK))) LOM2))
                                         
;(define (create-missile lom t) LOM0) ;stub

(define (create-missile lom t)
  (cond [(empty? lom) (cons (make-missile (tank-x t) (- HEIGHT (image-height TANK))) empty)]
        [else
         (cons (make-missile (tank-x t) (- HEIGHT (image-height TANK))) lom)]))


;; G -> Boolean
;; Stops the world when an invader reaches the end of the map
(check-expect (stop G0) false)
(check-expect (stop (make-game (list (make-invader 100 HEIGHT 10) (make-invader 100 100 10)) empty T0)) false)
(check-expect (stop (make-game (list (make-invader 100 100 10) (make-invader 100 (+ 1 HEIGHT) 10)) empty T0)) true)

;(define (stop g) false) ;stub

(define (stop g)
  (check-end (game-invaders g)))

;; LOI -> Boolean
;; Checks if any invaders int he list have reached the end of the map
(check-expect (check-end LOI0) false)
(check-expect (check-end (list (make-invader 10 10 10) (make-invader 10 HEIGHT 10))) false)
(check-expect (check-end (list (make-invader 10 10 10) (make-invader 10 (+ HEIGHT 1) 10))) true)

;(define (check-end loi) false) ;stub

(define (check-end loi)
  (cond [(empty? loi) false]
        [else
         (or (> (invader-y (first loi)) HEIGHT)
             (check-end (rest loi)))]))