from invoke import task


# No path for FloorPlan_Train6_4 from
# {'x': 6.0, 'y': 0.9009997, 'z': -3.6035533, 'rotation': {'x': 0.0, 'y': 179.999985, 'z': 0.0}, 'horizon': 0.0}
# to {'x': 5.25, 'y': 0.9009997, 'z': -4.25}

@task
def reachable_pos(ctx, scene="FloorPlan_Train2_3", editor_mode=False, local_build=False):
    import ai2thor.util.metrics as metrics
    import ai2thor.controller
    from ai2thor.util.metrics import get_shortest_path_to_point, get_shortest_path_to_object_type
    import copy
    gridSize = 0.25

    controller = ai2thor.controller.Controller(
        # rotateStepDegrees=45,
        visibilityDistance=1.0,
        gridSize=gridSize,
        # port=8200,
        # host='127.0.0.1',
        # local_executable_path=_local_build_path() if local_build else None,
        # start_unity=False if editor_mode else True,
        agentType="stochastic",
        continuousMode=True,
        # continuous=False,
        snapToGrid=False,
        agentMode="bot",
        scene=scene,
        width=300,
        height=300,

        fieldOfView=79.0,
        applyActionNoise=True,
        rotateStepDegrees=45.0,
        movementGaussianMu=1e-20,  # almost deterministic
        movementGaussianSigma=1e-20,  # almost deterministic
        rotateGaussianMu=1e-20,  # almost deterministic
        rotateGaussianSigma=1e-20,  # almost deterministic

        # continus=True
    )
    print("constoller.last_action Agent Pos: {}".format(controller.last_event.metadata["agent"]["position"]))

    evt = controller.step(action="GetReachablePositions", gridSize=gridSize)
    print("After GetReachable AgentPos: {}".format(evt.metadata['agent']['position']))
    print(evt.metadata["lastActionSuccess"])
    # print(evt.metadata["errorMessage"])
    reachable_pos = evt.metadata["actionReturn"]
    # print(evt.metadata["actionReturn"])

    evt = controller.step(
        dict(
            action="TeleportFull",
            x=8.0,
            y=reachable_pos[0]['y'],
            z=-2.25,
            rotation=dict(x=0, y=180.0, z=0),
            horizon=0.0,
        )
    )
    print("After teleport: {} {} {}".format(evt.metadata['agent']['position'], evt.metadata['agent']['rotation']['y'], evt.metadata['agent']['cameraHorizon']))
    source = copy.deepcopy(evt.metadata['agent']['position'])
    # source['y'] += 0.02
    print(get_shortest_path_to_point(controller, source, {'x': 9.0, 'y': 0.900999665, 'z': -3.75}))
    print("After path to point: {} {} {}".format(evt.metadata['agent']['position'], evt.metadata['agent']['rotation']['y'], evt.metadata['agent']['cameraHorizon']))

    evt = controller.step(
            action="TeleportFull",
            x=8.0,
            y=reachable_pos[0]['y'],
            z=-2.25,
            rotation=dict(x=0, y=180.0, z=0),
            horizon=0.0,
    )
    print(controller.last_event.metadata["lastActionSuccess"])
    print("After re-teleport: {} {} {}".format(evt.metadata['agent']['position'], evt.metadata['agent']['rotation']['y'], evt.metadata['agent']['cameraHorizon']))

    get_shortest_path_to_object_type(controller, "Television", source)  #, copy.deepcopy(evt.metadata['agent']['rotation']))
    evt = controller.last_event
    print("After path to object: {} {} {}".format(evt.metadata['agent']['position'], evt.metadata['agent']['rotation']['y'], evt.metadata['agent']['cameraHorizon']))

    evt = controller.step(
            action="TeleportFull",
            x=8.0,
            y=reachable_pos[0]['y'],
            z=-2.25,
            rotation=dict(x=0, y=180.0, z=0),
            horizon=0.0,
    )
    print(controller.last_event.metadata["lastActionSuccess"])
    print("After re-teleport: {} {} {}".format(evt.metadata['agent']['position'], evt.metadata['agent']['rotation']['y'], evt.metadata['agent']['cameraHorizon']))

    controller.stop()





    # TARGET_TYPES = sorted(
    #     [
    #         "AlarmClock",
    #         "Apple",
    #         "BaseballBat",
    #         "BasketBall",
    #         "Bowl",
    #         "GarbageCan",
    #         "HousePlant",
    #         "Laptop",
    #         "Mug",
    #         "Remote",
    #         "SprayBottle",
    #         "Television",
    #         "Vase",
    #         # 'AlarmClock',
    #         # 'Apple',
    #         # 'BasketBall',
    #         # 'Mug',
    #         # 'Television',
    #     ]
    # )
    #
    # TRAIN_SCENES = [
    #     "FloorPlan_Train%d_%d" % (wall + 1, furniture + 1)
    #     for wall in range(12)
    #     for furniture in range(5)
    # ]
    #
    # VALID_SCENES = [
    #     "FloorPlan_Val%d_%d" % (wall + 1, furniture + 1)
    #     for wall in range(3)
    #     for furniture in range(5)
    # ]
    #
    # env_config = dict(
    #     visibilityDistance=1.0,
    #     gridSize=gridSize,
    #     agentType="stochastic",
    #     continuousMode=True,
    #     snapToGrid=False,
    #     agentMode="bot",
    #     scene=scene,
    #     width=300,
    #     height=300,
    #     fieldOfView=79.0,
    #     applyActionNoise=True,
    #     rotateStepDegrees=45.0,
    #     movementGaussianMu=1e-20,  # almost deterministic
    #     movementGaussianSigma=1e-20,  # almost deterministic
    #     rotateGaussianMu=1e-20,  # almost deterministic
    #     rotateGaussianSigma=1e-20,  # almost deterministic
    # )
    #
    # from rl_robothor.robothor_task_samplers import ObjectNavTaskSampler, ObjectNavTask, PointNavTaskSampler, PointNavTask
    # from rl_ai2thor.ai2thor_sensors import RGBSensorThor, GoalObjectTypeThorSensor
    # import gym
    # from utils.system import LOGGER, init_logging
    # init_logging()
    #
    # SCREEN_SIZE = 224
    #
    # SENSORS = [
    #     RGBSensorThor(
    #         {
    #             "height": SCREEN_SIZE,
    #             "width": SCREEN_SIZE,
    #             "use_resnet_normalization": True,
    #             "uuid": "rgb_lowres",
    #         }
    #     ),
    #     GoalObjectTypeThorSensor({
    #         "object_types": TARGET_TYPES,
    #     }),
    # ]
    #
    # sampler_args = {
    #     "scenes": TRAIN_SCENES,
    #     "object_types": TARGET_TYPES,
    #     "sensors": SENSORS,
    #     "max_steps": 10,
    #     "action_space": gym.spaces.Discrete(len(ObjectNavTask.action_names())),
    #     "rewards_config": {
    #         "step_penalty": -0.01,
    #         "goal_success_reward": 10.0,
    #         "failed_stop_reward": 0.0,
    #         "shaping_weight": 1.0,  # applied to the decrease in distance to target
    #     },
    #     "env_args": env_config,
    # }
    #
    # sampler = ObjectNavTaskSampler(**sampler_args)
    # while True:
    #     task = sampler.next_task()
    #     # LOGGER.info("{}".format(task.task_info))
    #     # LOGGER.info("{}".format(task.env.dist_to_object(task.task_info['object_type'])))

@task
def dataset_stats(ctx, in_dataset="rl_robothor/data/val.json", out_dataset="rl_robothor/data/ordered_val.json"):
    import json
    import numpy as np

    from utils.system import init_logging, LOGGER

    init_logging()

    with open(in_dataset, "r") as f:
        orig = json.load(f)

    nsum = 0
    for object in set([ep["object_type"] for ep in orig]):
        message = [object + ":"]
        object_eps = [ep for ep in orig if ep["object_type"] == object]
        all_scenes = set([ep["scene"] for ep in object_eps])
        message.append(str(len(all_scenes)))
        message.append("scenes")
        for level in ["easy", "medium", "hard"]:
            neps = len([1 for ep in object_eps if ep["difficulty"] == level])
            message.append(str(neps))
            message.append(level)
            nsum += neps
        LOGGER.info(" ".join(message))
        del object_eps, all_scenes
    assert nsum == len(orig), "miscounted episodes: {} vs {}".format(nsum, len(orig))
    LOGGER.info("{} episodes in {}".format(nsum, in_dataset))

    for level in ["easy", "medium", "hard"]:
        message = [level + ":"]

        level_eps = [ep for ep in orig if ep["difficulty"] == level]

        message.append("episodes")
        message.append(str(len(level_eps)))

        message.append("mean_shortest_path_length")
        message.append(str(np.mean([ep["shortest_path_length"] for ep in level_eps])))

        message.append("mean_num_path_corners")
        message.append(str(np.mean([len(ep["shortest_path"]) for ep in level_eps])))

        LOGGER.info(" ".join(message))
        del message, level_eps
    obj_types = set([ep["object_type"] for ep in orig])
    LOGGER.info("{} object types: {}".format(len(obj_types), obj_types))

    all_scenes = sorted(set([ep["scene"] for ep in orig]))
    all_objects = sorted(set([ep["object_type"] for ep in orig]))
    nsum = 0
    for scene in all_scenes:
        scene_eps = [ep for ep in orig if ep["scene"] == scene]
        for level in ["easy", "medium", "hard"]:
            level_eps = [ep for ep in scene_eps if ep["difficulty"] == level]
            message = [scene, level]
            for object in all_objects:
                nobj = len([1 for ep in level_eps if ep["object_type"] == object])
                message += [str(nobj), object]
                nsum += nobj
            print(" ".join(message))
    assert nsum == len(orig), "miscounted episodes: {} vs {}".format(nsum, len(orig))

    # ordered = sorted(orig, key=lambda x: x["scene"])
    # LOGGER.info("{} episodes in {}".format(nsum, out_dataset))
    # with open(out_dataset, "w") as f:
    #     json.dump(ordered, f, indent=4, sort_keys=True)

    LOGGER.info("Done")

@task
def dataset_hists(ctx, train_dataset="rl_robothor/data/train.json", val_dataset="rl_robothor/data/val.json", sampling=6):  # 4 fo val only, 6 for train+val
    import json
    import numpy as np
    import matplotlib
    matplotlib.use('TkAgg')  # for GUI
    import matplotlib.pyplot as plt

    with open(val_dataset, "r") as f:
        orig = json.load(f)

    eps = {level: [ep for ep in orig if ep["difficulty"] == level] for level in ["easy", "medium", "hard"]}
    del orig

    with open(train_dataset, "r") as f:
        orig = json.load(f)

    # TODO Combine all episodes from val and train in the same chard
    for level in ["easy", "medium", "hard"]:
        eps[level] = [ep for ep in orig if ep["difficulty"] == level]
    del orig

    # def geo_dist(ep):
    #     path = ep["shortest_path"]
    #     dist = 0.0
    #     for it in range(len(path) - 1):
    #         sx, sz = (ep["shortest_path"][it][x] for x in ["x", "z"])
    #         tx, tz = (ep["shortest_path"][it + 1][x] for x in ["x", "z"])
    #         dist += np.sqrt((sx-tx)*(sx-tx) + (sz-tz)*(sz-tz))
    #     return dist

    def euc_dist(ep):
        sx, sz = (ep["initial_position"][x] for x in ["x", "z"])
        tx, tz = (ep["shortest_path"][-1][x] for x in ["x", "z"])  # assume we want it to be strictly smaller than the geodesic
        return np.sqrt((sx-tx)*(sx-tx) + (sz-tz)*(sz-tz))

    def dist_to_path(ep):
        sx, sz = (ep["initial_position"][x] for x in ["x", "z"])
        tx, tz = (ep["shortest_path"][0][x] for x in ["x", "z"])  # assume we want it to be strictly smaller than the geodesic
        return np.sqrt((sx-tx)*(sx-tx) + (sz-tz)*(sz-tz))

    # fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(10, 6), sharey=False)
    #
    # level2col={level: col for col, level in enumerate(["easy", "medium", "hard"])}
    # level2col["all"] = 3
    #
    # all_geo = []
    # all_euc = []
    # all_rat = []
    # for level in eps:
    #     geo = np.array([ep["shortest_path_length"] for ep in eps[level]])
    #     # geo = np.array([geo_dist(ep) for ep in eps[level]])
    #     # print(max(abs(geo - np.array([ep["shortest_path_length"] for ep in eps[level]]))))
    #     euc = np.array([euc_dist(ep) for ep in eps[level]])
    #     assert min(geo) > 0
    #     rat = euc / geo
    #
    #     all_geo.append(geo)
    #     all_euc.append(euc)
    #     all_rat.append(rat)
    #
    #     # for it, r in enumerate(zip(geo, rat)):
    #     #     if r[1] > 1.0:
    #     #         print(it, r)
    #
    #     nbins = int(np.sqrt(len(geo)) + 0.5) // sampling
    #     axes[0, level2col[level]].hist(geo, bins=nbins, alpha=0.5, label='geodesic {}'.format(level), density=False, histtype='bar', edgecolor='white')
    #     # axes[0, level2col[level]].legend(loc='upper right')
    #     axes[1, level2col[level]].hist(euc, bins=nbins, alpha=0.5, label='Euclidean {}'.format(level), density=False,
    #                                    histtype='bar', edgecolor='white')
    #     axes[2, level2col[level]].hist(rat, bins=nbins, range=(min(rat), 1.0), alpha=0.5, label='ratio {}'.format(level), density=False,
    #                                    histtype='bar', edgecolor='white')
    #
    # level = "all"
    # all_geo = np.concatenate(all_geo)
    # all_euc = np.concatenate(all_euc)
    # all_rat = np.concatenate(all_rat)
    # nbins = int(np.sqrt(len(all_geo)) + 0.5) // sampling
    # axes[0, level2col[level]].hist(all_geo, bins=nbins, alpha=0.5, label='geodesic {}'.format(level), density=False, histtype='bar', edgecolor='white')
    # # axes[0, level2col[level]].legend(loc='upper right')
    # axes[1, level2col[level]].hist(all_euc, bins=nbins, alpha=0.5, label='Euclidean {}'.format(level), density=False,
    #                                histtype='bar', edgecolor='white')
    # axes[2, level2col[level]].hist(all_rat, bins=nbins, range=(min(all_rat), 1.0), alpha=0.5, label='ratio {}'.format(level), density=False,
    #                                histtype='bar', edgecolor='white')
    #
    # axes[0, 0].set_ylabel('Geodesic')
    # axes[1, 0].set_ylabel('Euclidean')
    # axes[2, 0].set_ylabel('ratio')
    #
    # axes[-1, 0].set_xlabel('easy')
    # axes[-1, 1].set_xlabel('medium')
    # axes[-1, 2].set_xlabel('hard')
    # axes[-1, 3].set_xlabel('all')


    # fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(12, 6), sharey=False)

    all_geo = []
    all_euc = []
    all_rat = []
    for level in eps:
        geo = np.array([ep["shortest_path_length"] + dist_to_path(ep) for ep in eps[level]])
        # geo = np.array([geo_dist(ep) for ep in eps[level]])
        # print(max(abs(geo - np.array([ep["shortest_path_length"] for ep in eps[level]]))))
        euc = np.array([euc_dist(ep) for ep in eps[level]])
        assert min(geo) > 0
        rat = euc / geo

        all_geo.append(geo)
        all_euc.append(euc)
        all_rat.append(rat)

        # for it, r in enumerate(zip(geo, rat)):
        #     if r[1] > 1.0:
        #         print(it, r)


        # if level == "hard":
        #     thres = 1.0
        #     same = []
        #     nosame = []
        #     dist_same = []
        #     dist_nosame = []
        #
        #     from matplotlib import collections as mc
        #
        #     fig, ax = plt.subplots()
        #     colorsame = [(1, 0, 0, 1.0)]
        #     colornosame = [(0, 0, 1, 1.0)]
        #
        #     for it, r in enumerate(zip(geo, rat)):
        #         # if r[1] > 0.98:
        #         ep = eps["hard"][it]
        #         if len(ep["shortest_path"]) > 2:
        #             # print(it, r[1], ep["shortest_path"])
        #             sx, sz = (ep["initial_position"][x] for x in ["x", "z"])
        #             tx, tz = (ep["shortest_path"][-1][x] for x in["x", "z"])
        #             dv = (tx-sx, tz-sz)
        #             norm = np.sqrt(dv[0]*dv[0] + dv[1]*dv[1])
        #             assert norm > 0
        #             dv = (dv[0] / norm, dv[1] / norm)
        #             offset = (tx * sz - tz * sx) / norm
        #             clist = []
        #             lines = []
        #             for it in range(len(ep["shortest_path"]) - 1):
        #                 proj = dv[1] * ep["shortest_path"][it]['x'] - dv[0] * ep["shortest_path"][it]['z']
        #                 dist = abs(proj + offset)
        #                 clist.append(dist)
        #                 lines.append(
        #                     [(ep["shortest_path"][it]['x'], ep["shortest_path"][it]['z']),
        #                      (ep["shortest_path"][it + 1]['x'], ep["shortest_path"][it + 1]['z'])]
        #                 )
        #             if r[1] >= thres:
        #                 dist_same.append(r[0])
        #                 same.append(max(clist))
        #
        #                 import random
        #                 color = (random.random(), random.random(), random.random(), 1.0)
        #                 lc = mc.LineCollection(lines, colors=color, linewidths=2)
        #                 print(ep["shortest_path"], euc_dist(ep), r[0], ep["initial_position"], ep["shortest_path"][0])
        #                 print(ep)
        #                 ax.add_collection(lc)
        #
        #             else:
        #                 dist_nosame.append(r[0])
        #                 nosame.append(max(clist))
        #
        #                 # lc = mc.LineCollection(lines, colors=colornosame, linewidths=1)
        #                 # ax.add_collection(lc)
        #
        #     # nbins = int(np.sqrt((min(len(same), len(nosame)))) + 0.5)
        #
        #     # print(nbins)
        #
        #     # nbins = int(np.sqrt(len(same)) + 0.5)
        #     # plt.hist(dist_same, bins=nbins, alpha=0.5, label='same',
        #     #                        density=False, histtype='bar')
        #     # nbins = int(np.sqrt(len(nosame)) + 0.5)
        #     # plt.hist(dist_nosame, bins=nbins, alpha=0.5, label='nosame',
        #     #                        density=False, histtype='bar')
        #
        #
        #     ax.autoscale()
        #     ax.margins(0.1)
        #
        #
        #
        #                 # deltas = []
        #                 # for it in range(len(ep["shortest_path"]) - 1):
        #                 #     sx, sz = (ep["shortest_path"][it][x] for x in ["x", "z"])
        #                 #     tx, tz = (ep["shortest_path"][it + 1][x] for x in ["x", "z"])
        #                 #     if sx != tx:
        #                 #         deltas.append(('x', (sz-tz)/(sx-tx)))
        #                 #     elif sz != tz:
        #                 #         deltas.append(('z', (sx-tx)/(sz-tz)))
        #                 #     else:
        #                 #         assert False
        #                 # print(deltas, ep["shortest_path_length"])
        #
        # # nbins = int(np.sqrt(len(geo)) + 0.5) // sampling
        # # axes[0, level2col[level]].hist(geo, bins=nbins, alpha=0.5, label='geodesic {}'.format(level), density=False, histtype='bar', edgecolor='white')
        # # # axes[0, level2col[level]].legend(loc='upper right')
        # # axes[1, level2col[level]].hist(euc, bins=nbins, alpha=0.5, label='Euclidean {}'.format(level), density=False,
        # #                                histtype='bar', edgecolor='white')
        # # axes[2, level2col[level]].hist(rat, bins=nbins, range=(min(rat), 1.0), alpha=0.5, label='ratio {}'.format(level), density=False,
        # #                                histtype='bar', edgecolor='white')

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(13, 4), sharey=False)

    level = "all"
    all_geo = np.concatenate(all_geo)
    all_euc = np.concatenate(all_euc)
    all_rat = np.concatenate(all_rat)
    nbins = int(np.sqrt(len(all_geo)) + 0.5) // sampling
    axes[0].hist(all_geo, bins=nbins, alpha=1.0, label='geodesic {}'.format(level), density=False, histtype='bar', edgecolor=(199/255,209/255,227/255,1.0), color=(183/255,198/255,222/255,1.0))
    axes[0].set_xticks([])
    # axes[0, level2col[level]].legend(loc='upper right')
    axes[1].hist(all_euc, bins=nbins, alpha=1.0, label='Euclidean {}'.format(level), density=False, histtype='bar', edgecolor=(199/255,209/255,227/255,1.0), color=(183/255,198/255,222/255,1.0))
    axes[1].set_xticks([])
    # axes[2].hist(all_rat, bins=nbins, range=(min(all_rat), 1.0), alpha=0.5, label='ratio {}'.format(level), density=False, histtype='bar', edgecolor='white')
    axes[2].hist(all_rat, bins=nbins, alpha=1.0, label='ratio {}'.format(level), density=False, histtype='bar', edgecolor=(199/255,209/255,227/255,1.0), color=(183/255,198/255,222/255,1.0))
    axes[2].set_xticks([])

    axes[0].set_ylabel('RoboTHOR\nNumber of episodes', fontsize=16)

    axes[0].tick_params(axis='y', labelsize=14)
    axes[0].yaxis.set_ticks_position('none')
    axes[1].tick_params(axis='y', labelsize=14)
    axes[1].yaxis.set_ticks_position('none')
    axes[2].tick_params(axis='y', labelsize=14)
    axes[2].yaxis.set_ticks_position('none')
    # axes[1].yticks(fontsize=14)
    # axes[2].yticks(fontsize=14)

    fig.subplots_adjust(wspace=0.3, top=0.97, right=0.99, bottom=0.03, left=0.09)

    # print("Max geo:", max(all_geo), "min geo:", min(all_geo), "Max Euc:", max(all_euc), "min Euc:", min(all_euc))
    print("Max geo:", np.max(all_geo), "min geo:", np.min(all_geo), "Max Euc:", np.max(all_euc), "min Euc:", np.min(all_euc))

    plt.show()
