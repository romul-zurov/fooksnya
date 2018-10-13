#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import asyncio
from aiohttp import ClientSession

with open(os.path.join(os.path.dirname(__file__), 'conf', 'vk_access.json'), 'r') as _vk_conf:
    ACCESS_TOKEN = json.load(_vk_conf)['access_token']

API_VERSION = '5.60'  # '5.85'

PHOTO_THUMB_TYPE = tuple('xms')
PHOTO_SIZE_TYPE = tuple('wzyxms')
PHOTO_SIZE_TYPE_FULL = tuple('wzyqpoxms')


class VK(object):
    @staticmethod
    async def api_request(method, params=None):
        if not params:
            params = {}
        params.setdefault('v', API_VERSION)
        params.setdefault('access_token', ACCESS_TOKEN)
        url = f'https://api.VK.com/method/{method}'
        async with ClientSession() as session:
            async with session.get(url, params=params) as response:
                return await response.json()

    @staticmethod
    async def get_photos(owner_id, album_id='profile', photo_sizes=0):
        params = {
            'owner_id': owner_id,
            'album_id': str(album_id),
            'photo_sizes': photo_sizes,
        }
        res = await VK.api_request(method='photos.get', params=params)
        response = res.get('response', {})
        photos = response.get('items', [])
        return photos

    @staticmethod
    async def get_photos_thumb(**kvargs):
        photos = await VK.get_photos(**kvargs)
        imgs = []
        for img in photos:
            i = {k: img.get(k) for k in ('owner_id', 'id')}
            i['thumb'] = img.get(
                'photo_604', img.get(
                    'photo_130', img.get(
                        'photo_75', ''
                    )
                )
            )
            i['img'] = img.get(
                'photo_2560', img.get(
                    'photo_1280', img.get(
                        'photo_807', i.get(
                            'thumb', ''
                        )
                    )
                )
            )
            imgs.append(i)
        return imgs

    @staticmethod
    async def get_photos_thumb_sizes(owner_id, album_id='profile', **kvargs):
        kvargs.pop('photo_sizes', None)
        photos = await VK.get_photos(owner_id, album_id, photo_sizes=1, **kvargs)
        imgs = []
        for img in photos:
            i = {k: img.get(k) for k in ('owner_id', 'id')}
            sizes = img.get('sizes', [])

            # ~ print(sizes)

            def swh(types, prefix):
                # ~ print(types)
                src, w, h = '', '', ''
                for t in types:
                    for s in sizes:
                        if s.get('type') == t:
                            src = s.get('src', '')
                            w = s.get('width', '')
                            h = s.get('height', '')
                            break
                    if src:
                        break
                i[prefix + '_src'] = src
                i[prefix + '_width'] = w
                i[prefix + '_height'] = h

            swh(PHOTO_THUMB_TYPE, 'thumb')
            swh(PHOTO_SIZE_TYPE, 'img')
            # ~ print(i)
            imgs.append(i)
        return imgs


async def main():
    def print_list_of_dicts(list_of_dicts):
        for a in list_of_dicts:
            print('{')
            for kv in sorted(a.items()):
                print('\t%s:\t%s' % kv)
            print('},')
        print("Count: %s" % len(list_of_dicts))

    async def test_get_photos(log=True):
        photos = await VK.get_photos(owner_id=-2704617, album_id=107599236)
        if log:
            print('\nVK.get_photos(owner_id=-2704617, album_id=107599236):')
            print_list_of_dicts(photos)
        return photos

    async def test_thumb_and_maxsize(log=True):
        imgs = await VK.get_photos_thumb(owner_id=-2704617, album_id=107599236)
        if log:
            print_list_of_dicts(imgs)

    def test_photo_sizes(log=True):
        imgs = VK.get_photos(owner_id=-2704617, album_id=107599236,
                             photo_sizes=1)
        if log:
            print_list_of_dicts(imgs)

    async def test_get_photos_thumb_sizes(log=True):
        imgs = await VK.get_photos_thumb_sizes(owner_id=-2704617, album_id=107599236)
        if log:
            print_list_of_dicts(imgs)

    # await test_get_photos_thumb_sizes()
    await test_thumb_and_maxsize()
    # await test_get_photos()
    return 0


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
