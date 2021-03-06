# encoding=utf-8

from brunns.builder import Builder, a_boolean, a_string, an_integer, one_of
from brunns.builder.email import EmailBuilder
from brunns.builder.internet import UrlBuilder
from mbtest.imposters import (
    Copy,
    Imposter,
    InjectionResponse,
    Key,
    Lookup,
    Predicate,
    Proxy,
    Response,
    Stub,
    TcpResponse,
    UsingJsonpath,
    UsingRegex,
    UsingXpath,
)
from mbtest.imposters.imposters import Address, HttpRequest, SentEmail
from mbtest.imposters.predicates import AndPredicate, InjectionPredicate, OrPredicate, TcpPredicate


class PredicateBuilder(Builder):
    target = Predicate

    path = lambda: one_of(None, a_string())
    method = lambda: one_of(*Predicate.Method)
    query = lambda: one_of(None, {a_string(): a_string()})
    body = lambda: one_of(None, a_string())
    headers = lambda: one_of(None, {a_string(): a_string()})
    xpath = lambda: one_of(None, a_string())
    operator = lambda: one_of(*list(Predicate.Operator))
    case_sensitive = a_boolean


class OrPredicateBuilder(Builder):
    target = OrPredicate

    left = PredicateBuilder
    right = PredicateBuilder


class AndPredicateBuilder(Builder):
    target = AndPredicate

    left = PredicateBuilder
    right = PredicateBuilder


class TcpResponseBuilder(Builder):
    target = TcpResponse

    data = a_string


class UsingRegexBuilder(Builder):
    target = UsingRegex

    selector = a_string
    ignore_case = a_boolean


class UsingXpathBuilder(Builder):
    target = UsingXpath

    selector = a_string
    ns = a_string


class UsingJsonpathBuilder(Builder):
    target = UsingJsonpath

    selector = a_string


class CopyBuilder(Builder):
    target = Copy

    from_ = a_string
    into = a_string
    using = lambda: one_of(
        UsingRegexBuilder().build(), UsingXpathBuilder().build(), UsingJsonpathBuilder().build()
    )


class TcpPredicateBuilder(Builder):
    target = TcpPredicate

    data = a_string


class InjectionPredicateBuilder(Builder):
    target = InjectionPredicate
    inject = a_string()


class KeyBuilder(Builder):
    target = Key

    from_ = a_string
    using = lambda: one_of(
        UsingRegexBuilder().build(), UsingXpathBuilder().build(), UsingJsonpathBuilder().build()
    )
    index = lambda: an_integer(1, 50)


class LookupBuilder(Builder):
    target = Lookup

    key = KeyBuilder
    datasource_path = a_string
    datasource_key_column = a_string
    into = a_string


class ResponseBuilder(Builder):
    target = Response

    body = a_string
    status_code = lambda: one_of(
        200,
        201,
        202,
        203,
        204,
        205,
        206,
        207,
        208,
        226,
        300,
        301,
        302,
        303,
        304,
        305,
        307,
        308,
        400,
        401,
        402,
        403,
        404,
        405,
        406,
        407,
        408,
        409,
        410,
        411,
        412,
        413,
        414,
        415,
        416,
        417,
        418,
        421,
        422,
        423,
        424,
        426,
        428,
        429,
        431,
        444,
        451,
        499,
        500,
        501,
        502,
        503,
        504,
        505,
        506,
        507,
        508,
        510,
        511,
        599,
    )
    wait = lambda: one_of(an_integer(1, 500), None)
    repeat = lambda: one_of(an_integer(2, 50), None)
    headers = lambda: one_of(None, {a_string(): a_string()})
    mode = lambda: one_of(*Response.Mode)
    copy = lambda: one_of(None, CopyBuilder().build())
    decorate = lambda: one_of(None, a_string())
    lookup = lambda: one_of(None, LookupBuilder().build())
    shell_transform = lambda: one_of(None, a_string())


class InjectionResponseBuilder(Builder):
    target = InjectionResponse
    inject = a_string()


class StubBuilder(Builder):
    target = Stub

    predicates = lambda: [PredicateBuilder().build(), PredicateBuilder().build()]
    responses = lambda: [ResponseBuilder().build(), ResponseBuilder().build()]


class ProxyBuilder(Builder):
    target = Proxy

    to = UrlBuilder
    wait = lambda: one_of(None, an_integer(1, 1000))
    inject_headers = lambda: one_of(None, {a_string(): a_string()})
    mode = lambda: one_of(*Proxy.Mode)


class ImposterBuilder(Builder):
    target = Imposter

    stubs = lambda: [StubBuilder().build(), StubBuilder().build()]
    port = lambda: one_of(None, an_integer(1, 5000))
    protocol = one_of(*Imposter.Protocol)
    name = lambda: one_of(None, a_string())
    record_requests = a_boolean


class HttpRequestBuilder(Builder):
    target = HttpRequest

    method = lambda: one_of(*Predicate.Method).name
    path = lambda: UrlBuilder().build().path
    query = lambda: {a_string(): a_string(), a_string(): a_string()}
    headers = lambda: {a_string(): a_string(), a_string(): a_string()}
    body = lambda: one_of(None, a_string())


class AddressBuilder(Builder):
    target = Address

    address = EmailBuilder
    name = a_string


class SentEmailBuilder(Builder):
    target = SentEmail

    from_ = lambda: [AddressBuilder().build()]
    to = lambda: [AddressBuilder().build(), AddressBuilder().build()]
    cc = lambda: [AddressBuilder().build(), AddressBuilder().build()]
    bcc = lambda: [AddressBuilder().build(), AddressBuilder().build()]
    subject = a_string
    text = a_string
