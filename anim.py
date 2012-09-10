from spyral import animations
from spyral.sprite import Sprite, Group
from collections import defaultdict
from spyral import animations

class Animation(object):
    def __init__(self, property,
                       animation,
                       duration = 1.0,
                       absolute = True,
                       ):
        """
        *animation* determines the animation you wish to apply
        
        *absolute* determines whether the property should be in
        absolute coordinates, or whether this is an offset
        animation that should be added to the current property.
        
        *duration* is the amount of time the animation should take.
        
        *property* is the property of the sprite you wish to animate.
        Special properties are "x" and "y" which refer to the first
        and second parts of the position tuple.
        """
        
        # Idea: These animators could be used for camera control
        # at some point. Everything should work pretty much the same.
        
        properties = ['x', 'y', 'image', 'scale']
        self.property = property
        self.animation = animation
        self.duration = duration
        self.absolute = absolute
        
    def evaluate(self, sprite, progress):
        progress = progress/self.duration
        value = self.animation(progress)
        return value            

class AnimationGroup(Group):
    def __init__(self, *args):
        Group.__init__(self, *args)
        self._animations = defaultdict(list)
        self._progress = {}
        self._on_complete = {}
        self._start_state = {}
    
    def add_animation(self, sprite, animation, on_complete = None):
        for a in self._animations[sprite]:
            if a.property == animation.property:
                raise ValueError("Cannot animate on propety %s twice" % animation.property)
        self._animations[sprite].append(animation)
        self._progress[(sprite, animation)] = 0
        self._on_complete[(sprite, animation)] = on_complete
        if animation.absolute is False:
            self._start_state[(sprite, animation)] = getattr(sprite, animation.property)
        
    def update(self, dt):
        completed = []
        on_completes = []
        for sprite in self._sprites:
            for animation in self._animations[sprite]:
                self._progress[(sprite, animation)] += dt
                progress = self._progress[(sprite, animation)]
                if progress > animation.duration:
                    progress = animation.duration
                    completed.append((sprite, animation))
    
                value = animation.evaluate(sprite, progress)
                if animation.absolute is False:
                    value = value + self._start_state[(sprite, animation)]
                setattr(sprite, animation.property, value)

        for sprite, animation in completed:
            self._animations[sprite].remove(animation)
            del self._progress[(sprite, animation)]
            c = self._on_complete[(sprite, animation)]
            on_completes.append(c)
            del self._on_complete[(sprite, animation)]
            try:
                del self._start_state[(sprite, animation)]
            except KeyError:
                pass
        d = [c() for c in on_completes if c is not None]
        Group.update(self, dt)

class AnimationSprite(Sprite):
    """
    TODO: Should verify the group it is added to is an AnimationGroup,
    and enforce the one group per sprite rule
    """
    def animate(self, animation, on_complete = None):
        self._groups[0].add_animation(self, animation, on_complete)