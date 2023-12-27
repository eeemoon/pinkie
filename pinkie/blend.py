class BlendMode:
    def blend(self, bg, fg):
        raise NotImplementedError()
    
    def compose(self, bg, fg, bits: int):
        if bg._bits != fg._bits:
            raise ValueError(f"can not blend colors with different size")
        
        return self.blend(bg, fg)
        
    

class Normal(BlendMode):
    def blend(self, bg, fg):
        return fg