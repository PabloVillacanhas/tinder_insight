# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = tinder_profile_from_dict(json.loads(json_string))
from functools import reduce
from typing import Any, Optional, List, TypeVar, Type, cast, Callable
from enum import Enum
from uuid import UUID
from datetime import datetime
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


class School:
    displayed: bool
    name: str

    def __init__(self, displayed: bool, name: str) -> None:
        self.displayed = displayed
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> 'School':
        assert isinstance(obj, dict)
        displayed = from_bool(obj.get("displayed"))
        name = from_str(obj.get("name"))
        return School(displayed, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["displayed"] = from_bool(self.displayed)
        result["name"] = from_str(self.name)
        return result


class Job:
    title: School

    def __init__(self, title: School) -> None:
        self.title = title

    @staticmethod
    def from_dict(obj: Any) -> 'Job':
        assert isinstance(obj, dict)
        title = School.from_dict(obj.get("title"))
        return Job(title)

    def to_dict(self) -> dict:
        result: dict = {}
        result["title"] = to_class(School, self.title)
        return result


class Algo:
    width_pct: float
    x_offset_pct: float
    height_pct: float
    y_offset_pct: float

    def __init__(self, width_pct: float, x_offset_pct: float, height_pct: float, y_offset_pct: float) -> None:
        self.width_pct = width_pct
        self.x_offset_pct = x_offset_pct
        self.height_pct = height_pct
        self.y_offset_pct = y_offset_pct

    @staticmethod
    def from_dict(obj: Any) -> 'Algo':
        assert isinstance(obj, dict)
        width_pct = from_float(obj.get("width_pct"))
        x_offset_pct = from_float(obj.get("x_offset_pct"))
        height_pct = from_float(obj.get("height_pct"))
        y_offset_pct = from_float(obj.get("y_offset_pct"))
        return Algo(width_pct, x_offset_pct, height_pct, y_offset_pct)

    def to_dict(self) -> dict:
        result: dict = {}
        result["width_pct"] = to_float(self.width_pct)
        result["x_offset_pct"] = to_float(self.x_offset_pct)
        result["height_pct"] = to_float(self.height_pct)
        result["y_offset_pct"] = to_float(self.y_offset_pct)
        return result


class Face:
    algo: Algo
    bounding_box_percentage: float

    def __init__(self, algo: Algo, bounding_box_percentage: float) -> None:
        self.algo = algo
        self.bounding_box_percentage = bounding_box_percentage

    @staticmethod
    def from_dict(obj: Any) -> 'Face':
        assert isinstance(obj, dict)
        algo = Algo.from_dict(obj.get("algo"))
        bounding_box_percentage = from_float(obj.get("bounding_box_percentage"))
        return Face(algo, bounding_box_percentage)

    def to_dict(self) -> dict:
        result: dict = {}
        result["algo"] = to_class(Algo, self.algo)
        result["bounding_box_percentage"] = to_float(self.bounding_box_percentage)
        return result


class CropInfo:
    user: Optional[Algo]
    algo: Optional[Algo]
    processed_by_bullseye: bool
    user_customized: bool
    faces: Optional[List[Face]]

    def __init__(self, user: Optional[Algo], algo: Optional[Algo], processed_by_bullseye: bool, user_customized: bool, faces: Optional[List[Face]]) -> None:
        self.user = user
        self.algo = algo
        self.processed_by_bullseye = processed_by_bullseye
        self.user_customized = user_customized
        self.faces = faces

    @staticmethod
    def from_dict(obj: Any) -> 'CropInfo':
        assert isinstance(obj, dict)
        user = from_union([Algo.from_dict, from_none], obj.get("user"))
        algo = from_union([Algo.from_dict, from_none], obj.get("algo"))
        processed_by_bullseye = from_bool(obj.get("processed_by_bullseye"))
        user_customized = from_bool(obj.get("user_customized"))
        faces = from_union([lambda x: from_list(Face.from_dict, x), from_none], obj.get("faces"))
        return CropInfo(user, algo, processed_by_bullseye, user_customized, faces)

    def to_dict(self) -> dict:
        result: dict = {}
        result["user"] = from_union([lambda x: to_class(Algo, x), from_none], self.user)
        result["algo"] = from_union([lambda x: to_class(Algo, x), from_none], self.algo)
        result["processed_by_bullseye"] = from_bool(self.processed_by_bullseye)
        result["user_customized"] = from_bool(self.user_customized)
        result["faces"] = from_union([lambda x: from_list(lambda x: to_class(Face, x), x), from_none], self.faces)
        return result


class Version(Enum):
    D_HASH_V1_0 = "dHash v1.0"
    P_HASH_V1_0 = "pHash v1.0"


class Hash:
    version: Version
    value: float

    def __init__(self, version: Version, value: float) -> None:
        self.version = version
        self.value = value

    @staticmethod
    def from_dict(obj: Any) -> 'Hash':
        assert isinstance(obj, dict)
        version = Version(obj.get("version"))
        value = from_float(obj.get("value"))
        return Hash(version, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["version"] = to_enum(Version, self.version)
        result["value"] = to_float(self.value)
        return result


class ProcessedFile:
    url: str
    height: int
    width: int

    def __init__(self, url: str, height: int, width: int) -> None:
        self.url = url
        self.height = height
        self.width = width

    @staticmethod
    def from_dict(obj: Any) -> 'ProcessedFile':
        assert isinstance(obj, dict)
        url = from_str(obj.get("url"))
        height = from_int(obj.get("height"))
        width = from_int(obj.get("width"))
        return ProcessedFile(url, height, width)

    def to_dict(self) -> dict:
        result: dict = {}
        result["url"] = from_str(self.url)
        result["height"] = from_int(self.height)
        result["width"] = from_int(self.width)
        return result


class Photo:
    id: UUID
    type: str
    created_at: datetime
    updated_at: datetime
    crop_info: CropInfo
    url: str
    processed_files: List[ProcessedFile]
    file_name: str
    extension: str
    fb_id: str
    webp_qf: List[int]
    rank: int
    score: float
    win_count: int
    phash: Hash
    dhash: Hash

    def __init__(self, id: UUID, type: str, created_at: datetime, updated_at: datetime, crop_info: CropInfo, url: str, processed_files: List[ProcessedFile], file_name: str, extension: str, fb_id: str, webp_qf: List[int], rank: int, score: float, win_count: int, phash: Hash, dhash: Hash) -> None:
        self.id = id
        self.type = type
        self.created_at = created_at
        self.updated_at = updated_at
        self.crop_info = crop_info
        self.url = url
        self.processed_files = processed_files
        self.file_name = file_name
        self.extension = extension
        self.fb_id = fb_id
        self.webp_qf = webp_qf
        self.rank = rank
        self.score = score
        self.win_count = win_count
        self.phash = phash
        self.dhash = dhash

    @staticmethod
    def from_dict(obj: Any) -> 'Photo':
        assert isinstance(obj, dict)
        id = UUID(obj.get("id"))
        type = from_str(obj.get("type"))
        created_at = from_datetime(obj.get("created_at"))
        updated_at = from_datetime(obj.get("updated_at"))
        crop_info = CropInfo.from_dict(obj.get("crop_info"))
        url = from_str(obj.get("url"))
        processed_files = from_list(ProcessedFile.from_dict, obj.get("processedFiles"))
        file_name = from_str(obj.get("fileName"))
        extension = from_str(obj.get("extension"))
        fb_id = from_str(obj.get("fbId"))
        webp_qf = from_list(from_int, obj.get("webp_qf"))
        rank = from_int(obj.get("rank"))
        score = from_float(obj.get("score"))
        win_count = from_int(obj.get("win_count"))
        phash = Hash.from_dict(obj.get("phash"))
        dhash = Hash.from_dict(obj.get("dhash"))
        return Photo(id, type, created_at, updated_at, crop_info, url, processed_files, file_name, extension, fb_id, webp_qf, rank, score, win_count, phash, dhash)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = str(self.id)
        result["type"] = from_str(self.type)
        result["created_at"] = self.created_at.isoformat()
        result["updated_at"] = self.updated_at.isoformat()
        result["crop_info"] = to_class(CropInfo, self.crop_info)
        result["url"] = from_str(self.url)
        result["processedFiles"] = from_list(lambda x: to_class(ProcessedFile, x), self.processed_files)
        result["fileName"] = from_str(self.file_name)
        result["extension"] = from_str(self.extension)
        result["fbId"] = from_str(self.fb_id)
        result["webp_qf"] = from_list(from_int, self.webp_qf)
        result["rank"] = from_int(self.rank)
        result["score"] = to_float(self.score)
        result["win_count"] = from_int(self.win_count)
        result["phash"] = to_class(Hash, self.phash)
        result["dhash"] = to_class(Hash, self.dhash)
        return result

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Photo):
            return False

        return self.score.__eq__(other.score) and self.id.__eq__(other.id)


class Pos:
    at: int
    lat: float
    lon: float

    def __init__(self, at: int, lat: float, lon: float) -> None:
        self.at = at
        self.lat = lat
        self.lon = lon

    @staticmethod
    def from_dict(obj: Any) -> 'Pos':
        assert isinstance(obj, dict)
        at = from_int(obj.get("at"))
        lat = from_float(obj.get("lat"))
        lon = from_float(obj.get("lon"))
        return Pos(at, lat, lon)

    def to_dict(self) -> dict:
        result: dict = {}
        result["at"] = from_int(self.at)
        result["lat"] = to_float(self.lat)
        result["lon"] = to_float(self.lon)
        return result


class Country:
    name: str
    cc: str
    alpha3: str

    def __init__(self, name: str, cc: str, alpha3: str) -> None:
        self.name = name
        self.cc = cc
        self.alpha3 = alpha3

    @staticmethod
    def from_dict(obj: Any) -> 'Country':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        cc = from_str(obj.get("cc"))
        alpha3 = from_str(obj.get("alpha3"))
        return Country(name, cc, alpha3)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["cc"] = from_str(self.cc)
        result["alpha3"] = from_str(self.alpha3)
        return result


class PosInfo:
    country: Country
    timezone: str

    def __init__(self, country: Country, timezone: str) -> None:
        self.country = country
        self.timezone = timezone

    @staticmethod
    def from_dict(obj: Any) -> 'PosInfo':
        assert isinstance(obj, dict)
        country = Country.from_dict(obj.get("country"))
        timezone = from_str(obj.get("timezone"))
        return PosInfo(country, timezone)

    def to_dict(self) -> dict:
        result: dict = {}
        result["country"] = to_class(Country, self.country)
        result["timezone"] = from_str(self.timezone)
        return result


class TinderProfile:
    id: str
    age_filter_max: int
    age_filter_min: int
    badges: List[Any]
    bio: str
    birth_date: datetime
    blend: str
    create_date: datetime
    discoverable: bool
    discoverable_party: str
    distance_filter: int
    email: str
    facebook_id: str
    gender: int
    gender_filter: int
    hide_ads: bool
    hide_age: bool
    hide_distance: bool
    spotify_connected: bool
    interested_in: List[int]
    jobs: List[Job]
    name: str
    photos: List[Photo]
    photo_optimizer_enabled: bool
    ping_time: datetime
    pos: Pos
    pos_info: PosInfo
    schools: List[School]
    show_gender_on_profile: bool
    can_create_squad: bool

    def __init__(self, id: str, age_filter_max: int, age_filter_min: int, badges: List[Any], bio: str, birth_date: datetime, blend: str, create_date: datetime, discoverable: bool, discoverable_party: str, distance_filter: int, email: str, facebook_id: str, gender: int, gender_filter: int, hide_ads: bool, hide_age: bool, hide_distance: bool, spotify_connected: bool, interested_in: List[int], jobs: List[Job], name: str, photos: List[Photo], photo_optimizer_enabled: bool, ping_time: datetime, pos: Pos, pos_info: PosInfo, schools: List[School], show_gender_on_profile: bool, can_create_squad: bool) -> None:
        self.id = id
        self.age_filter_max = age_filter_max
        self.age_filter_min = age_filter_min
        self.badges = badges
        self.bio = bio
        self.birth_date = birth_date
        self.blend = blend
        self.create_date = create_date
        self.discoverable = discoverable
        self.discoverable_party = discoverable_party
        self.distance_filter = distance_filter
        self.email = email
        self.facebook_id = facebook_id
        self.gender = gender
        self.gender_filter = gender_filter
        self.hide_ads = hide_ads
        self.hide_age = hide_age
        self.hide_distance = hide_distance
        self.spotify_connected = spotify_connected
        self.interested_in = interested_in
        self.jobs = jobs
        self.name = name
        self.photos = photos
        self.photo_optimizer_enabled = photo_optimizer_enabled
        self.ping_time = ping_time
        self.pos = pos
        self.pos_info = pos_info
        self.schools = schools
        self.show_gender_on_profile = show_gender_on_profile
        self.can_create_squad = can_create_squad

    @staticmethod
    def from_dict(obj: Any) -> 'TinderProfile':
        assert isinstance(obj, dict)
        id = from_str(obj.get("_id"))
        age_filter_max = from_int(obj.get("age_filter_max"))
        age_filter_min = from_int(obj.get("age_filter_min"))
        badges = from_list(lambda x: x, obj.get("badges"))
        bio = from_str(obj.get("bio"))
        birth_date = from_datetime(obj.get("birth_date"))
        blend = from_str(obj.get("blend"))
        create_date = from_datetime(obj.get("create_date"))
        discoverable = from_bool(obj.get("discoverable"))
        discoverable_party = from_str(obj.get("discoverable_party"))
        distance_filter = from_int(obj.get("distance_filter"))
        email = from_str(obj.get("email"))
        facebook_id = from_str(obj.get("facebook_id"))
        gender = from_int(obj.get("gender"))
        gender_filter = from_int(obj.get("gender_filter"))
        hide_ads = from_bool(obj.get("hide_ads"))
        hide_age = from_bool(obj.get("hide_age"))
        hide_distance = from_bool(obj.get("hide_distance"))
        spotify_connected = from_bool(obj.get("spotify_connected"))
        interested_in = from_list(from_int, obj.get("interested_in"))
        jobs = from_list(Job.from_dict, obj.get("jobs"))
        name = from_str(obj.get("name"))
        photos = from_list(Photo.from_dict, obj.get("photos"))
        photo_optimizer_enabled = from_bool(obj.get("photo_optimizer_enabled"))
        ping_time = from_datetime(obj.get("ping_time"))
        pos = Pos.from_dict(obj.get("pos"))
        pos_info = PosInfo.from_dict(obj.get("pos_info"))
        schools = from_list(School.from_dict, obj.get("schools"))
        show_gender_on_profile = from_bool(obj.get("show_gender_on_profile"))
        can_create_squad = from_bool(obj.get("can_create_squad"))
        return TinderProfile(id, age_filter_max, age_filter_min, badges, bio, birth_date, blend, create_date, discoverable, discoverable_party, distance_filter, email, facebook_id, gender, gender_filter, hide_ads, hide_age, hide_distance, spotify_connected, interested_in, jobs, name, photos, photo_optimizer_enabled, ping_time, pos, pos_info, schools, show_gender_on_profile, can_create_squad)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_str(self.id)
        result["age_filter_max"] = from_int(self.age_filter_max)
        result["age_filter_min"] = from_int(self.age_filter_min)
        result["badges"] = from_list(lambda x: x, self.badges)
        result["bio"] = from_str(self.bio)
        result["birth_date"] = self.birth_date.isoformat()
        result["blend"] = from_str(self.blend)
        result["create_date"] = self.create_date.isoformat()
        result["discoverable"] = from_bool(self.discoverable)
        result["discoverable_party"] = from_str(self.discoverable_party)
        result["distance_filter"] = from_int(self.distance_filter)
        result["email"] = from_str(self.email)
        result["facebook_id"] = from_str(self.facebook_id)
        result["gender"] = from_int(self.gender)
        result["gender_filter"] = from_int(self.gender_filter)
        result["hide_ads"] = from_bool(self.hide_ads)
        result["hide_age"] = from_bool(self.hide_age)
        result["hide_distance"] = from_bool(self.hide_distance)
        result["spotify_connected"] = from_bool(self.spotify_connected)
        result["interested_in"] = from_list(from_int, self.interested_in)
        result["jobs"] = from_list(lambda x: to_class(Job, x), self.jobs)
        result["name"] = from_str(self.name)
        result["photos"] = from_list(lambda x: to_class(Photo, x), self.photos)
        result["photo_optimizer_enabled"] = from_bool(self.photo_optimizer_enabled)
        result["ping_time"] = self.ping_time.isoformat()
        result["pos"] = to_class(Pos, self.pos)
        result["pos_info"] = to_class(PosInfo, self.pos_info)
        result["schools"] = from_list(lambda x: to_class(School, x), self.schools)
        result["show_gender_on_profile"] = from_bool(self.show_gender_on_profile)
        result["can_create_squad"] = from_bool(self.can_create_squad)
        return result

    def __eq__(self, other):
        if not isinstance(other, TinderProfile):
            return False

        if len(self.photos) != len(other.photos):
            return False
        return reduce(lambda a, b: a and b, map(lambda x, y: x == y, self.photos, other.photos))

def tinder_profile_from_dict(s: Any) -> TinderProfile:
    return TinderProfile.from_dict(s)


def tinder_profile_to_dict(x: TinderProfile) -> Any:
    return to_class(TinderProfile, x)
