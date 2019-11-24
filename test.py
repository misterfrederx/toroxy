import time

import config
import privoxy
import tor

# print('init tor repo')
# tors = IndexedDirManager(config.TOR_DIR, config.TOR_SUBDIR_BASE_NAME)
# print('init privoxy repo')
# privoxyes = IndexedDirManager(config.PRIVOXY_DIR, config.PRIVOXY_SUBDIR_BASE_NAME)

print('build instances')
t = tor.build(config.TOR_DIR, 1)
p = privoxy.build(config.PRIVOXY_DIR, 1)

print('launch')
t.run()
p.run()

print('wait 10 seconds before shutting down')
time.sleep(10)

print('shutting down')
p.stop()
t.stop()

print('finish.')