"""
Cookie Clicker Simulator
"""
import math
import simpleplot
# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._total_cookies_ = 0.0
        self._current_cookies_ = 0.0
        self._current_time_ = 0.0
        self._current_cps_ = 1.0
        self._history_ = [(0.0, None, 0.0, 0.0)]

    def __str__(self):
        """
        Return human readable state
        """
        str_time = "Time: " + str(self._current_time_)
        str_current = " Current Cookies: " + str(self._current_cookies_)
        str_cps = " CPS: " + str(self._current_cps_)
        str_total = " Total Cookies: " + str(self._total_cookies_)
        str_history = " History: " + str(self._history_)
        return str_time + str_current + str_cps + str_total+str_history

    def get_cookies(self):
        """
        Return current number of cookies
        (not total number of cookies)

        Should return a float
        """
        return float(self._current_cookies_)

    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return float(self._current_cps_)

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return float(self._current_time_)

    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        copy_history = []
        for state in self._history_:
            copy_history.append(state)
        return copy_history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._current_cookies_ >= cookies:
            return 0.0
        time = math.ceil((cookies - self._current_cookies_) / self._current_cps_)
        return float(time)

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0:
            self._current_cookies_ += time * self._current_cps_
            self._total_cookies_ += time * self._current_cps_
            self._current_time_ += time

    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies_ >= cost:
            self._current_cps_ += additional_cps
            self._current_cookies_ -= cost
            self._history_.append((self._current_time_, item_name, cost, self._total_cookies_))


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    current_info = build_info.clone()
    state = ClickerState()
    while state.get_time() <= duration:
        #Use specific founction to determin which item to buy next.
        item = map(strategy, [state.get_cookies()], [state.get_cps()], [state.get_history()], [duration - state.get_time()], [current_info])[0]
        if not item:
            break
        #Determin how much time you need to buy this item, then wait that time, but the item and update the buildinfo
        cost = current_info.get_cost(item)
        wait_time = state.time_until(cost)
        if wait_time + state.get_time() > duration:
            break
        state.wait(wait_time)
        state.buy_item(item, cost, current_info.get_cps(item))
        current_info.update_item(item)
    state.wait(duration - state.get_time())
    return state


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    cost_list = [build_info.get_cost(item) for item in build_info.build_items()]
    cheap = min(cost_list)
    afford = cookies + cps * time_left
    if cheap <= afford:
        item = build_info.build_items()[cost_list.index(cheap)]
        return item
    else:
        return None

def afford_or_not(cost_list_unit):
    """
    compare cost and cookies
    """
    cost, cookies = cost_list_unit[1], cost_list_unit[2]
    return cookies >= cost



def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    # item_list = [[item, cost, left_cookies], ...]
    left_cookies = cookies + cps * time_left
    item_list = [[item, build_info.get_cost(item), left_cookies] for item in build_info.build_items()]
    afford = filter(afford_or_not, item_list)
    if not afford:
        return None
    expens = max(afford)
    expens_idx = afford.index(expens)
    item = afford[expens_idx][0]
    return item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    The profit of buying an item = item.cps * (left_time - waiting_time)
    So make most profit, then we get the best strategy.
    """
    # item_list = [[item, cost, left_cookies], ...]
    # filter out the items we can't buy in the rest of the game.
    left_cookies = cookies + cps * time_left
    item_list = [[item, build_info.get_cost(item), left_cookies] for item in build_info.build_items()]
    afford = filter(afford_or_not, item_list)

    # If we can't afford any item, reutrn None
    if not afford:
        return None

    #Create a profit dict = {item: profit,  ...}
    profit = {}
    for item in afford:
        cost = build_info.get_cost(item[0])
        time_wait = 0.0
        if cost >= cookies:
            time_wait = float(math.ceil((cost - cookies) / cps))
        profit[item[0]] = build_info.get_cps(item[0]) * (time_left - time_wait) / build_info.get_cost(item[0])

    #Find the most profit(best) item.
    best_item = profit.keys()[0]
    for key, value in profit.items():
        if profit[best_item] < value:
            best_item = key
    return best_item

def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """
    #run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)


run()