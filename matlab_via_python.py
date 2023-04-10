import matlab.engine
eng = matlab.engine.start_matlab()
eng.meat_leftovers_algorithm(nargout=0)
eng.quit()