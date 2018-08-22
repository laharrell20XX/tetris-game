from core import *
import pytest


def test_empty_grid_drop_dot():
    ''' drops an active dot block in an empty grid'''
    assert Grid([], ActiveBlock(3, 5, Block([(0,0)]))).drop() == \
           Grid([], ActiveBlock(3, 4, Block([(0,0)])))


def test_occupied_grid_drop_dot():
    ''' drops an active dot block in a grid with another dot '''
    assert Grid([Block([(0,0)])], ActiveBlock(3, 5, Block([(0,0)]))).drop() == \
           Grid([Block([(0,0)])], ActiveBlock(3, 4, Block([(0,0)])))


def test_empty_grid_move_dot_left():
    ''' moves an active dot block to the left in an empty grid'''
    assert Grid([], ActiveBlock(3, 5, Block([(0,0)]))).move('left') == \
           Grid([], ActiveBlock(2, 5, Block([(0,0)])))


def test_empty_grid_move_dot_right():
    ''' moves an active dot block to the right in an empty grid'''
    assert Grid([], ActiveBlock(3, 5, Block([(0,0)]))).move('right') == \
           Grid([], ActiveBlock(4, 5, Block([(0,0)])))


def test_empty_grid_move_nonsense_direction():
    ''' calls move with an invalid direction argument. '''
    assert Grid([], ActiveBlock(3, 5, Block(
        [(0, 0)]))).move('not left or right') is None


def test_rotate_dot():
    g = Grid([], ActiveBlock(3, 5, Block([(0, 0)])))
    assert g.rotate() == g


def test_rotate_L():
    assert Grid([], ActiveBlock(3, 5, Block([(0, 2), (0, 1), (0, 0), (1, 0)]))).rotate() == \
           Grid([], ActiveBlock(3, 5, Block([(2, 0), (1, 0), (0, 0), (0, -1)])))


def test_four_rotations_is_identity():
    g = Grid([], ActiveBlock(3, 5, Block([(0, 2), (0, 1), (0, 0), (1, 0)])))
    assert g.rotate().rotate().rotate().rotate() == g


def test_valid_corners_current():
    # bottom left
    assert not Grid([], ActiveBlock(-1, 0, Block([(0, 0)]))).is_valid()
    assert not Grid([], ActiveBlock(-1, -1, Block([(0, 0)]))).is_valid()
    assert not Grid([], ActiveBlock(0, -1, Block([(0, 0)]))).is_valid()
    assert Grid([], ActiveBlock(0, 0, Block([(0, 0)]))).is_valid()
    # bottom right
    assert not Grid([], ActiveBlock(WIDTH, 0, Block([(0, 0)]))).is_valid()
    assert not Grid([], ActiveBlock(WIDTH, -1, Block([(0, 0)]))).is_valid()
    assert not Grid([], ActiveBlock(WIDTH - 1, -1, Block([(0, 0)]))).is_valid()
    assert Grid([], ActiveBlock(WIDTH - 1, 0, Block([(0, 0)]))).is_valid()
    # top right
    assert not Grid([], ActiveBlock(WIDTH, HEIGHT, Block([(0, 0)]))).is_valid()
    assert Grid([], ActiveBlock(WIDTH - 1, HEIGHT, Block([(0, 0)]))).is_valid()
    assert not Grid([], ActiveBlock(WIDTH, HEIGHT - 1, Block([(0, 0)
                                                              ]))).is_valid()
    assert Grid([], ActiveBlock(WIDTH - 1, HEIGHT - 1,
                                Block([(0, 0)]))).is_valid()
    # top left
    assert Grid([], ActiveBlock(0, HEIGHT, Block([(0, 0)]))).is_valid()
    assert not Grid([], ActiveBlock(-1, HEIGHT, Block([(0, 0)]))).is_valid()
    assert not Grid([], ActiveBlock(-1, HEIGHT - 1, Block([(0, 0)
                                                           ]))).is_valid()
    assert Grid([], ActiveBlock(0, HEIGHT - 1, Block([(0, 0)]))).is_valid()


def test_valid_corners_placed():
    # bottom left
    assert not Grid([Block([
        (-1, 0)
    ])], ActiveBlock(WIDTH // 2, HEIGHT // 2, Block([(0, 0)]))).is_valid()
    assert not Grid([Block([
        (0, -1)
    ])], ActiveBlock(WIDTH // 2, HEIGHT // 2, Block([(0, 0)]))).is_valid()
    assert not Grid([Block([
        (-1, -1)
    ])], ActiveBlock(WIDTH // 2, HEIGHT // 2, Block([(0, 0)]))).is_valid()
    assert Grid([Block([(0, 0)])],
                ActiveBlock(WIDTH // 2, HEIGHT // 2, Block([(0,
                                                             0)]))).is_valid()
    # bottom right
    assert not Grid([Block([
        (WIDTH, 0)
    ])], ActiveBlock(WIDTH // 2, HEIGHT // 2, Block([(0, 0)]))).is_valid()
    assert not Grid([Block([
        (WIDTH, -1)
    ])], ActiveBlock(WIDTH // 2, HEIGHT // 2, Block([(0, 0)]))).is_valid()
    assert not Grid([Block([
        (WIDTH - 1, -1)
    ])], ActiveBlock(WIDTH // 2, HEIGHT // 2, Block([(0, 0)]))).is_valid()
    assert Grid([Block([(WIDTH - 1, 0)])],
                ActiveBlock(WIDTH // 2, HEIGHT // 2, Block([(0,
                                                             0)]))).is_valid()
    # top right
    assert not Grid([Block([
        (WIDTH, HEIGHT)
    ])], ActiveBlock(WIDTH // 2, HEIGHT // 2, Block([(0, 0)]))).is_valid()
    assert Grid([Block([(WIDTH - 1, HEIGHT)])],
                ActiveBlock(WIDTH // 2, HEIGHT // 2, Block([(0,
                                                             0)]))).is_valid()
    assert not Grid([Block([
        (WIDTH, HEIGHT - 1)
    ])], ActiveBlock(WIDTH // 2, HEIGHT // 2, Block([(0, 0)]))).is_valid()
    assert Grid([Block([(WIDTH - 1, HEIGHT - 1)])],
                ActiveBlock(WIDTH // 2, HEIGHT // 2, Block([(0,
                                                             0)]))).is_valid()
    # top left
    assert Grid([Block([(0, HEIGHT)])],
                ActiveBlock(WIDTH // 2, HEIGHT // 2, Block([(0,
                                                             0)]))).is_valid()
    assert not Grid([Block([
        (-1, HEIGHT)
    ])], ActiveBlock(WIDTH // 2, HEIGHT // 2, Block([(0, 0)]))).is_valid()
    assert not Grid([Block([
        (-1, HEIGHT - 1)
    ])], ActiveBlock(WIDTH // 2, HEIGHT // 2, Block([(0, 0)]))).is_valid()
    assert Grid([Block([(0, HEIGHT - 1)])],
                ActiveBlock(WIDTH // 2, HEIGHT // 2, Block([(0,
                                                             0)]))).is_valid()


def test_empty_is_occupied_all():
    g = Grid([], ActiveBlock(0, 0, Block([(0, 0)])))
    assert not any(
        g.is_occupied((x, y)) for x in range(WIDTH) for y in range(HEIGHT))


def test_dot_is_occupied_all():
    occupied_posn = (WIDTH // 2, HEIGHT // 2)
    unoccupied_posns = {(x, y)
                        for x in range(WIDTH)
                        for y in range(HEIGHT)} - {occupied_posn}
    g = Grid([Block([occupied_posn])], ActiveBlock(0, 0, Block([(0, 0)])))
    assert g.is_occupied(occupied_posn)
    assert not any(g.is_occupied(p) for p in unoccupied_posns)


def test_empty_clear_full_rows():
    g = Grid([], ActiveBlock(0, 0, Block([(0, 0)])))
    assert g.clear_full_rows() == g


def test_bottom_full_dots_clear_full_rows():
    g = Grid([Block([(x, 0)]) for x in range(WIDTH)],
             ActiveBlock(0, 0, Block([(0, 0)])))
    assert g.clear_full_rows() == Grid([], ActiveBlock(0, 0, Block([(0, 0)])))


def test_bottom_two_full_dots_clear_full_rows():
    g = Grid([Block([(x, y)]) for x in range(WIDTH) for y in (0, 1)],
             ActiveBlock(0, 0, Block([(0, 0)])))
    assert g.clear_full_rows() == Grid([], ActiveBlock(0, 0, Block([(0, 0)])))


def test_place_block_dot():
    g = Grid([], ActiveBlock(1, 2, Block([(3, 4)])))
    assert g.place_block() == Grid([Block([(4, 6)])], None)