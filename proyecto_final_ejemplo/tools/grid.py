class Grid:
    
    def __init__(self, frame_width, frame_height) -> None:
        self.frame_w = frame_width
        self.frame_h = frame_height
        
    def rect_at(self, row, col):
        x, y = self.frame_w * col, self.frame_h * row
        return x, y, self.frame_w, self.frame_h
    
    def rects_at_row(self, row, col, end_frame, row_offset=0, col_offset=0):
        return [self.rect_at(row + row_offset, col + i + col_offset) for i in range(end_frame)]

    def rects_at_col(self, row, col, end_frame, row_offset=0, col_offset=0):
        return [self.rect_at(row + i + row_offset, col + col_offset) for i in range(end_frame)]
